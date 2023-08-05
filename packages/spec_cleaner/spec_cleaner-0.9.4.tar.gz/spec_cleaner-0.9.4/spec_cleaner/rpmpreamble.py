# vim: set ts=4 sw=4 et: coding=UTF-8

import re

from .rpmsection import Section
from .rpmexception import RpmException
from .rpmhelpers import sort_uniq
from .dependency_parser import DependencyParser

class RpmPreamble(Section):

    """
        Only keep one empty line for many consecutive ones.
        Reorder lines.
        Fix bad licenses.
        Use one line per BuildRequires/Requires/etc.
        Standardize BuildRoot.

        This one is a bit tricky since we reorder things. We have a notion of
        paragraphs, categories, and groups.

        A paragraph is a list of non-empty lines. Conditional directives like
        %if/%else/%endif also mark paragraphs. It contains categories.
        A category is a list of lines on the same topic. It contains a list of
        groups.
        A group is a list of lines where the first few ones are comment lines,
        and the last one is a normal line.

        This means that comments will stay attached to one
        line, even if we reorder the lines.
    """

    category_to_key = {
        'name': 'Name',
        'version': 'Version',
        'release': 'Release',
        'license': 'License',
        'summary': 'Summary',
        # The localized summary can contain various values, so it can't be here
        'url': 'Url',
        'group': 'Group',
        'source': 'Source',
        'nosource': 'NoSource',
        'patch': 'Patch',
        'buildrequires': 'BuildRequires',
        'conflicts': 'Conflicts',
        'prereq': 'PreReq',
        'requires': 'Requires',
        'requires_eq': '%requires_eq',
        'recommends': 'Recommends',
        'suggests': 'Suggests',
        'enhances': 'Enhances',
        'supplements': 'Supplements',
        # Provides/Obsoletes cannot be part of this since we want to keep them
        # mixed, so we'll have to specify the key when needed
        'buildroot': 'BuildRoot',
        'buildarch': 'BuildArch',
        'exclusivearch': 'ExclusiveArch',
        'excludearch': 'ExcludeArch',
    }

    categories_order = [
        'define',
        'bconds',
        'bcond_conditions',
        'name',
        'version',
        'release',
        'summary',
        'summary_localized',
        'license',
        'group',
        'url',
        'source',
        'nosource',
        'patch',
        'buildrequires',
        'requires',
        'requires_eq',
        'prereq',
        'requires_phase',  # this is Requires(pre/post/...)
        'recommends',
        'suggests',
        'enhances',
        'supplements',
        'conflicts',
        'provides_obsoletes',
        'buildroot',
        'buildarch',
        'exclusivearch',
        'excludearch',
        'misc',
        'build_conditions',
        'conditions',
    ]

    # categories that are sorted based on value in them
    categories_with_sorted_package_tokens = [
        'buildrequires',
        'prereq',
        'requires',
        'requires_eq',
        'recommends',
        'suggests',
        'enhances',
        'supplements',
        'conflicts',
    ]

    # categories that are sorted based on key value (eg Patch0 before Patch1)
    categories_with_sorted_keyword_tokens = [
        'source',
        'patch',
    ]

    def __init__(self, options):
        Section.__init__(self, options)
        # Old storage
        self._oldstore = []
        # Is the parsed variable multiline (ending with \)
        self.multiline = False
        # Are we inside of conditional or not
        self.condition = False
        # Is the condition with define/global variables
        self._condition_define = False
        # Is the condition based probably on bcond evaluation
        self._condition_bcond = False
        # do we want pkgconfig and others?
        self.pkgconfig = options['pkgconfig']
        self.perl = options['perl']
        self.cmake = options['cmake']
        self.tex = options['tex']
        # are we supposed to keep empty lines intact?
        self.keep_space = options['keep_space']
        # dict of license replacement options
        self.license_conversions = options['license_conversions']
        # dict of pkgconfig and other conversions
        self.pkgconfig_conversions = options['pkgconfig_conversions']
        self.perl_conversions = options['perl_conversions']
        self.cmake_conversions = options['cmake_conversions']
        self.tex_conversions = options['tex_conversions']
        # list of allowed groups
        self.allowed_groups = options['allowed_groups']
        # start the object
        self._start_paragraph()
        # initialize list of groups that need to pass over conversion fixer
        self.categories_with_package_tokens = self.categories_with_sorted_package_tokens[:]
        # these packages actually need fixing after we sent the values to
        # reorder them
        self.categories_with_package_tokens.append('provides_obsoletes')
        # license handling
        self.subpkglicense = options['subpkglicense']
        self.license = options['license']
        # pkgconfig requirement detection
        self.br_pkgconfig_required = False

        # simple categories matching
        self.category_to_re = {
            'name': self.reg.re_name,
            'version': self.reg.re_version,
            # license need fix replacment
            'summary': self.reg.re_summary,
            'url': self.reg.re_url,
            'group': self.reg.re_group,
            'nosource': self.reg.re_nosource,
            # for source, we have a special match to keep the source number
            # for patch, we have a special match to keep the patch number
            'buildrequires': self.reg.re_buildrequires,
            'conflicts': self.reg.re_conflicts,
            # for prereq we append warning comment so we don't mess it there
            'requires': self.reg.re_requires,
            'recommends': self.reg.re_recommends,
            'suggests': self.reg.re_suggests,
            'enhances': self.reg.re_enhances,
            'supplements': self.reg.re_supplements,
            # for provides/obsoletes, we have a special case because we group them
            # for build root, we have a special match because we force its value
            'buildarch': self.reg.re_buildarch,
            'excludearch': self.reg.re_excludearch,
            'exclusivearch': self.reg.re_exclusivearch,
        }

        # deprecated definitions that we no longer want to see
        self.category_to_clean = {
            'vendor': self.reg.re_vendor,
            'autoreqprov': self.reg.re_autoreqprov,
            'epoch': self.reg.re_epoch,
            'icon': self.reg.re_icon,
            'copyright': self.reg.re_copyright,
            'packager': self.reg.re_packager,
            'debugpkg': self.reg.re_debugpkg,
            'prefix': self.reg.re_preamble_prefix,
        }

    def _start_paragraph(self):
        self.paragraph = {}
        for i in self.categories_order:
            self.paragraph[i] = []
        self.current_group = []

    def start_subparagraph(self):
        # store the main content and clean up
        self._oldstore.append(self.paragraph)
        self._start_paragraph()

    def _add_group(self, group):
        """
        Actually store the lines from groups to resulting output
        """
        t = type(group)
        if t == str:
            return [group]
        elif t == list:
            x = []
            for subgroup in group:
                x += self._add_group(subgroup)
            return x
        else:
            raise RpmException('Unknown type of group in preamble: %s' % t)

    def _sort_helper_key(self, a):
        t = type(a)
        if t == str:
            key = a
        elif t == list:
            # if this is a list then all items except last are comment or whitespace
            key = a[-1]
        else:
            raise RpmException('Unknown type during sort: %s' % t)

        # Special case is the category grouping where we have to get the number in
        # after the value
        if self.reg.re_patch.match(key):
            match = self.reg.re_patch.match(key)
            key = int(match.group(2))
        elif self.reg.re_source.match(key):
            match = self.reg.re_source.match(key)
            value = match.group(1)
            if not value:
                value = '0'
            key = int(value)
        # Put brackety ()-style deps at the end of the list, after all other
        elif self.reg.re_brackety_requires.search(key):
            key = '1' + key
        else:
            key = '0' + key
        return key

    def end_subparagraph(self, endif=False):
        lines = self._end_paragraph()
        if len(self.paragraph['define']) > 0 or \
           len(self.paragraph['bconds']) > 0:
            self._condition_define = True
        self.paragraph = self._oldstore.pop(-1)
        self.paragraph['conditions'] += lines

        # If we are on endif we check the condition content
        # and if we find the defines we put it on top.
        if endif or not self.condition:
            # check if we are doing the ppc64 migration and delete it
            if not self.minimal and \
                 isinstance(self.paragraph['conditions'][0], list) and \
                 len(self.paragraph['conditions']) == 3 and \
                 self.paragraph['conditions'][0][0] == '# bug437293' and \
                 self.paragraph['conditions'][1].endswith('64bit'):
                self.paragraph['conditions'] = []
            if self._condition_define:
                # If we have define conditions and possible bcond start
                # we need to put it bellow bcond definitions as otherwise
                # the switches do not have any effect
                if self._condition_bcond:
                    self.paragraph['bcond_conditions'] += self.paragraph['conditions']
                elif len(self.paragraph['define']) == 0:
                    self.paragraph['bconds'] += self.paragraph['conditions']
                else:
                    self.paragraph['define'] += self.paragraph['conditions']
                # in case the nested condition contains define we consider all parents
                # to require to be on top too;
                if len(self._oldstore) == 0:
                    self._condition_define = False
            else:
                self.paragraph['build_conditions'] += self.paragraph['conditions']

            # bcond must be reseted when on top and can be set even outside of the
            # define scope. So reset it here always
            if len(self._oldstore) == 0:
                self._condition_bcond = False
            self.paragraph['conditions'] = []

    def _find_pkgconfig_statements(self, listname):
        for i in self.paragraph[listname]:
            if isinstance(i, str):
                if 'pkgconfig(' in i and not self._find_pkgconfig_declarations(listname):
                    return True
            elif isinstance(i, list):
                for j in i:
                    if 'pkgconfig(' in j and not self._find_pkgconfig_declarations(listname):
                        return True
        return False

    def _find_pkgconfig_declarations(self, listname):
        for i in self.paragraph[listname]:
            if isinstance(i, str):
                if 'pkgconfig ' in i or i.endswith('pkgconfig'):
                    return True
            elif isinstance(i, list):
                for j in i:
                    if 'pkgconfig ' in j or j.endswith('pkgconfig'):
                        return True
        return False

    def _end_paragraph(self, needs_license=False):
        lines = []

        # add license to the package if missing and needed
        if needs_license:
            if not self.paragraph['license']:
                self.license = self._fix_license(self.license)
                self._add_line_value_to('license', self.license)

        # Check if we need the pkgconfig
        if not self.br_pkgconfig_required and \
           self._find_pkgconfig_statements('buildrequires'):
            self.br_pkgconfig_required = True
        # only in case we are in main scope
        if not self._oldstore:
            if self.br_pkgconfig_required and not self._find_pkgconfig_declarations('buildrequires'):
                self._add_line_value_to('buildrequires', 'pkgconfig')

        # sort based on category order
        for i in self.categories_order:
            sorted_list = []
            # sort-out within the ordered groups based on the key
            if i in self.categories_with_sorted_package_tokens:
                self.paragraph[i].sort(key=self._sort_helper_key)
                self.paragraph[i] = sort_uniq(self.paragraph[i])
            # sort-out within the ordered groups based on the keyword
            if i in self.categories_with_sorted_keyword_tokens:
                self.paragraph[i].sort(key=self._sort_helper_key)
            for group in self.paragraph[i]:
                sorted_list += self._add_group(group)
            # now check if we need to add comment for the prereq
            if i == 'prereq' and not self.minimal:
                sorted_list = self._verify_prereq_message(sorted_list)
            lines += sorted_list
        if self.current_group:
            # the current group was not added to any category. It's just some
            # random stuff that should be at the end anyway.
            lines += self._add_group(self.current_group)
            self.current_group = []
        return lines

    def _fix_license(self, value):
        # split using 'or', 'and' and parenthesis, ignore empty strings
        licenses = []
        for a in re.split(r'(\(|\)| and | or (?!later))', value):
            if a != '':
                licenses.append(a)
        if not licenses:
            licenses.append(value)

        for (index, my_license) in enumerate(licenses):
            my_license = self.strip_useless_spaces(my_license)
            my_license = my_license.replace('ORlater', 'or later')
            my_license = my_license.replace('ORsim', 'or similar')
            my_license = my_license.rstrip(';')
            my_license = self.reg.re_license_semicolon.sub(' and ', my_license)
            if my_license in self.license_conversions:
                my_license = self.license_conversions[my_license]
            licenses[index] = my_license

        # create back new string with replaced licenses
        s = ' '.join(licenses).replace("( ", "(").replace(" )", ")")
        return s

    def _split_name_and_version(self, value):
        # split the name and version from the requires element
        if self.reg.re_version_separator.match(value):
            match = self.reg.re_version_separator.match(value)
            pkgname = match.group(1)
            version = match.group(2)
        if not version:
            version = ''
        return pkgname, version

    def _fix_pkgconfig_name(self, value):
        # we just rename pkgconfig names to one unified one working everywhere
        pkgname, version = self._split_name_and_version(value)
        if pkgname == 'pkgconfig(pkg-config)' or \
           pkgname == 'pkg-config':
            # If we have pkgconfig dep in pkgconfig it is nuts, replace it
            return 'pkgconfig{0}'.format(version)
        else:
            return value

    def _pkgname_to_pkgconfig(self, value):
        # we just want the pkgname if we have version string there
        # and for the pkgconfig deps we need to put the version into
        # the braces
        pkgname, version = self._split_name_and_version(value)
        pkgconfig = []
        if pkgname == 'pkgconfig':
            return [value]
        if pkgname not in self.pkgconfig_conversions:
            # first check if the package is in the replacements
            return [value]
        else:
            # first split the pkgconfig data
            pkgconf_list = self.pkgconfig_conversions[pkgname].split()
            # then add each pkgconfig to the list
            # print pkgconf_list
            for j in pkgconf_list:
                pkgconfig.append('pkgconfig({0}){1}'.format(j, version))
        return pkgconfig

    def _pkgname_to_brackety(self, value, name, conversions):
        # we just want the pkgname if we have version string there
        # and for the pkgconfig deps we need to put the version into
        # the braces
        pkgname, version = self._split_name_and_version(value)
        converted = []
        if pkgname not in conversions:
            # first check if the package is in the replacements
            return [value]
        else:
            # first split the data
            convers_list = conversions[pkgname].split()
            # then add each pkgconfig to the list
            # print pkgconf_list
            for j in convers_list:
                converted.append('{0}({1}){2}'.format(name, j, version))
        return converted

    def _fix_list_of_packages(self, value, category):
        # we do fix the package list only if there is no rpm call there on line
        # otherwise print there warning about nicer content and skip
        if self.reg.re_rpm_command.search(value):
            if not self.previous_line.startswith('#') and not self.minimal:
                self.current_group.append('# FIXME: Use %requires_eq macro instead')
            return [value]
        tokens = DependencyParser(value).flat_out()
        # loop over all and do formatting as we can get more deps for one
        expanded = []
        for token in tokens:
            # there is allowed syntax => and =< ; hidious
            token = token.replace('=<', '<=')
            token = token.replace('=>', '>=')
            # we also skip all various rpm-macroed content as it
            # is usually not easy to determine how that should be
            # split
            if token.startswith('%'):
                expanded.append(token)
                continue
            # cleanup whitespace
            token = token.replace(' ', '')
            token = re.sub(r'([<>]=?|=)', r' \1 ', token)
            if not token:
                continue
            # replace pkgconfig name first
            token = self._fix_pkgconfig_name(token)
            # in scriptlets we most probably do not want the converted deps
            if category != 'prereq':
                # here we go with descending priority to find match and replace
                # the strings by some optimistic value of brackety dep
                # priority is based on the first come first serve
                if self.pkgconfig:
                    token = self._pkgname_to_pkgconfig(token)
                # checking if it is not list is simple avoidance of running
                # over already converted values
                if type(token) is not list and self.perl:
                    token = self._pkgname_to_brackety(token, 'perl', self.perl_conversions)
                if type(token) is not list and self.tex:
                    token = self._pkgname_to_brackety(token, 'tex', self.tex_conversions)
                if type(token) is not list and self.cmake:
                    token = self._pkgname_to_brackety(token, 'cmake', self.cmake_conversions)
            if isinstance(token, str):
                expanded.append(token)
            else:
                expanded += token
        # and then sort them :)
        expanded.sort()
        return expanded

    def _verify_prereq_message(self, elements):
        """
            Verify if the prereq is present in the Requires(*) and add the fixme
            comment if needed
        """
        message = '# FIXME: use proper Requires(pre/post/preun/...)'

        # Check first if we have prereq values included
        if not any("PreReq" in s for s in elements):
            return elements

        # Verify the message is not already present
        if any(message in s for s in elements):
            return elements

        # add the message on the first position after any whitespace
        location = next(i for i, j in enumerate(elements) if j)
        elements.insert(location, message)

        return elements

    def _add_line_value_to(self, category, value, key=None):
        """
            Change a key-value line, to make sure we have the right spacing.

            Note: since we don't have a key <-> category matching, we need to
            redo one. (Eg: Provides and Obsoletes are in the same category)
        """
        keylen = len('BuildRequires:  ')

        if key:
            pass
        elif category in self.category_to_key:
            key = self.category_to_key[category]
        else:
            raise RpmException('Unhandled category in preamble: %s' % category)

        # append : only if the thing is not known macro
        if not key.startswith('%'):
            key += ':'
        # if the key is already longer then just add one space
        if len(key) >= keylen:
            key += ' '
        # fillup rest of the alignment if key is shorter than muster
        while len(key) < keylen:
            key += ' '

        if category in self.categories_with_package_tokens:
            values = self._fix_list_of_packages(value, category)
        else:
            values = [value]

        for value in values:
            line = key + value
            self._add_line_to(category, line)

    def _add_line_to(self, category, line):
        if self.current_group:
            self.current_group.append(line)
            self.paragraph[category].append(self.current_group)
            self.current_group = []
        else:
            self.paragraph[category].append(line)

        self.previous_line = line

    def add(self, line):
        line = self._complete_cleanup(line)

        # if the line is empty, just skip it, unless keep_space is true
        if not self.keep_space and len(line) == 0:
            return

        # if it is multiline variable then we need to append to previous content
        # also multiline is allowed only for define lines so just cheat and
        # know ahead
        elif self.multiline:
            self._add_line_to('define', line)
            # if it is no longer trailed with backslash stop
            if not line.endswith('\\'):
                self.multiline = False
            return

        # If we match the if else or endif we create subgroup
        # this is basically our class again until we match
        # else where we mark end of paragraph or endif
        # which mark the end of our subclass and that we can
        # return the data to our main class for at-bottom placement
        elif self.reg.re_if.match(line) or self.reg.re_codeblock.match(line):
            self._add_line_to('conditions', line)
            self.condition = True
            # check for possibility of the bcond conditional
            if "%{with" in line or "%{without" in line:
                self._condition_bcond = True
            self.start_subparagraph()
            self.previous_line = line
            return

        elif self.reg.re_else.match(line):
            if self.condition:
                self._add_line_to('conditions', line)
                self.end_subparagraph()
                self.start_subparagraph()
            self.previous_line = line
            return

        elif self.reg.re_endif.match(line) or self.reg.re_endcodeblock.match(line):
            self._add_line_to('conditions', line)
            # Set conditions to false only if we are
            # closing last of the nested ones
            if len(self._oldstore) == 1:
                self.condition = False
            self.end_subparagraph(True)
            self.previous_line = line
            return

        elif self.reg.re_comment.match(line):
            if line or self.previous_line:
                self.current_group.append(line)
                self.previous_line = line
            return

        elif self.reg.re_source.match(line):
            match = self.reg.re_source.match(line)
            self._add_line_value_to('source', match.group(2), key='Source%s' % match.group(1))
            return

        elif self.reg.re_patch.match(line):
            match = self.reg.re_patch.match(line)
            # convert Patch: to Patch0:
            if match.group(2) == '':
                zero = '0'
            else:
                zero = ''
            self._add_line_value_to('patch', match.group(3), key='%sPatch%s%s' % (match.group(1), zero, match.group(2)))
            return

        elif self.reg.re_bcond_with.match(line):
            self._add_line_to('bconds', line)
            return

        elif self.reg.re_define.match(line) or self.reg.re_global.match(line) or self.reg.re_onelinecond.match(line):
            if line.endswith('\\'):
                self.multiline = True
            # if we are kernel and not multiline we need to be at bottom, so
            # lets use misc section, otherwise go for define
            if not self.multiline and line.find("kernel_module") >= 0:
                self._add_line_to('misc', line)
            else:
                self._add_line_to('define', line)
            return

        elif self.reg.re_requires_eq.match(line):
            match = self.reg.re_requires_eq.match(line)
            self._add_line_value_to('requires_eq', match.group(1))
            return

        elif self.reg.re_prereq.match(line):
            match = self.reg.re_prereq.match(line)
            self._add_line_value_to('prereq', match.group(1))
            return

        elif self.reg.re_requires_phase.match(line):
            match = self.reg.re_requires_phase.match(line)
            # Put the requires content properly as key for formatting
            self._add_line_value_to('prereq', match.group(2), key='Requires{0}'.format(match.group(1)))
            return

        elif self.reg.re_provides.match(line):
            match = self.reg.re_provides.match(line)
            self._add_line_value_to('provides_obsoletes', match.group(1), key='Provides')
            return

        elif self.reg.re_obsoletes.match(line):
            match = self.reg.re_obsoletes.match(line)
            self._add_line_value_to('provides_obsoletes', match.group(1), key='Obsoletes')
            return

        elif self.reg.re_buildroot.match(line):
            # we only are fine with buildroot only once
            if len(self.paragraph['buildroot']) == 0:
                self._add_line_value_to('buildroot', '%{_tmppath}/%{name}-%{version}-build')
            return

        elif self.reg.re_license.match(line):
            # first convert the license string to proper format and then append
            match = self.reg.re_license.match(line)
            value = match.groups()[len(match.groups()) - 1]
            value = self._fix_license(value)
            # only store subpkgs if they have different licenses
            if not (type(self).__name__ == 'RpmPackage' and not self.subpkglicense):
                self._add_line_value_to('license', value)
            return

        elif self.reg.re_release.match(line):
            match = self.reg.re_release.match(line)
            value = match.group(1)
            if re.search(r'[a-zA-Z\s]', value):
                self._add_line_value_to('release', value)
            else:
                self._add_line_value_to('release', '0')
            return

        elif self.reg.re_summary_localized.match(line):
            match = self.reg.re_summary_localized.match(line)
            # we need to know what language we need
            language = match.group(1)
            # and what value is there
            content = match.group(2)
            self._add_line_value_to('summary_localized', content, key='Summary{0}'.format(language))
            return

        elif self.reg.re_group.match(line):
            match = self.reg.re_group.match(line)
            value = match.group(1)
            if not self.minimal:
                if self.previous_line and not self.previous_line.startswith('# FIXME') and value not in self.allowed_groups:
                    self.current_group.append('# FIXME: use correct group, see "https://en.opensuse.org/openSUSE:Package_group_guidelines"')
            self._add_line_value_to('group', value)
            return

        # loop for all other matching categories which
        # do not require special attention
        else:
            # cleanup
            for (category, regexp) in self.category_to_clean.items():
                match = regexp.match(line)
                if match:
                    return

            # simple matching
            for (category, regexp) in self.category_to_re.items():
                match = regexp.match(line)
                if match:
                    # instead of matching first group as there is only one,
                    # take the last group
                    # (so I can have more advanced regexp for RPM tags)
                    self._add_line_value_to(category, match.groups()[len(match.groups()) - 1])
                    return

            self._add_line_to('misc', line)

    def output(self, fout, newline=True, new_class=None):
        lines = self._end_paragraph(self.subpkglicense)
        self.lines += lines
        Section.output(self, fout, newline, new_class)
