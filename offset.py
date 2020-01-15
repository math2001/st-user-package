import sublime
import sublime_plugin


STATUS_KEY = "offset-plugin"


class OffsetListener(sublime_plugin.ViewEventListener):
    @classmethod
    def is_applicable(self, settings):
        return True

    @classmethod
    def applies_to_primary_view_only(self):
        return False

    def on_selection_modified_async(self):
        offsets = []
        for region in self.view.sel():
            offsets.append(str(region.a))
            if region.b != region.a:
                offsets[-1] = "{} => {}".format(region.a, region.b)
        self.view.set_status(STATUS_KEY, "Offset: " + ",".join(offsets))
