import sublime
import unittest

SINGLE_SCOPE = 1

class SyntaxTestCase(unittest.TestCase):
    def setUp(self):
        self.view = sublime.active_window().new_file()

    def tearDown(self):
        if self.view:
            self.view.set_scratch(True)
            self.view.window().focus_view(self.view)
            self.view.window().run_command("close_file")

    def set_syntax_file(self, syntax_file):
        assert(self.view)
        self.view.set_syntax_file(syntax_file)

    def set_text(self, string):
        self.view.run_command("select_all")
        self.view.run_command("left_delete")
        self.view.run_command("insert", {"characters": string})

    def set_default_scope(self, default_scope):
        self.default_scope = default_scope

    def has_scope(self, region, scope):
        pos = region.begin()
        scope_region = self.view.extract_scope(pos)
        if not scope_region.contains(region):
            return False
        return self.view.score_selector(pos, scope) > 0

    def has_single_scope(self, region, scope):
        if not self.has_scope(region, scope):
            return False
        return len(self.view.scope_name(region.begin()).split()) == 1

    def verify_pattern(self, pattern, scope, flags):
        regions = self.view.find_all(pattern)
        self.assertTrue(regions, 'Cannot find pattern /{}/'.format(pattern))
        check = self.has_single_scope if flags == SINGLE_SCOPE else self.has_scope
        for region in regions:
            self.assertTrue(check(region, scope),
                'Text "{}" found by /{}/ does not match scope "{}"'.format(
                    self.view.substr(region),
                    pattern,
                    scope
                    )
                )

    def verify_scope(self, patterns, scope, flags = 0):
        if type(patterns) is not list:
            patterns = [ patterns ]
        for pattern in patterns:
            self.verify_pattern(pattern, scope, flags)

    def verify_default(self, patterns):
        self.verify_scope(patterns, self.default_scope, SINGLE_SCOPE)

    # def verify_scopes(self, scopes):
    #     for scope in scopes:
    #         self.verify_scope(*scope)

    # def verify(self, text, scopes):
    #     self.set_text(text)
    #     self.verify_scopes(scopes)
