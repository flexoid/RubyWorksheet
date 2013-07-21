import sublime, sublime_plugin, subprocess, os.path

class RubyWorksheetExecuteCommand(sublime_plugin.TextCommand):

  # It shouldn't be like this
  def __init__(self, arg):
    sublime_plugin.TextCommand.__init__(self, arg)
    self.ruby_path = sublime.load_settings("RubyWorksheet.sublime-settings").get("ruby_path", "ruby")

  def run(self, edit):
    script_path = os.path.join(sublime.packages_path(), "RubyWorksheet", "pry_repl.rb")

    proc = subprocess.Popen([self.ruby_path, script_path], shell=False, stdin=subprocess.PIPE,
      stdout=subprocess.PIPE, close_fds=True, universal_newlines=True, bufsize=0)

    line_rigions = self.view.split_by_newlines(sublime.Region(0, self.view.size()))
    comments = []
    position = 0
    for line_rigion in line_rigions:
      line = self.view.substr(line_rigion)
      position += len(line) + 1

      proc.stdin.write(line + "\n")
      proc.stdout.flush()

      out = proc.stdout.readline()
      status = proc.stdout.readline()

      if len(line) > 1:
        str_for_insert = out.rstrip('\n')
        comments.append([str_for_insert, position])

    proc.kill();

    offset = 0
    for comment in comments:
      if len(comment[0]) > 1:
        line_to_insert = " " * 10 + "# " + comment[0]
        self.view.replace(edit, sublime.Region(comment[1] + offset - 1, comment[1] + offset - 1), line_to_insert)
        offset += len(line_to_insert)
