from threading import RLock

from terminalsize import get_terminal_size

lock = RLock()


class ProgressBarFormatter:
    def __init__(self, prefix='', suffix='', percent_decimal=1):
        self.char_length = 0
        self.prefix = prefix
        self.suffix = suffix
        self.percent_decimal = percent_decimal
        self.bars = []

    def add_bar(self, bar):
        lock.acquire()
        self.bars.append(bar)
        self._update_char_length()
        lock.release()

    def _update_char_length(self):
        if len(self.bars) == 0:
            return
        terminal_width, _ = get_terminal_size()
        separator_length = len(self.bars) - 1 if len(self.bars) >= 2 else 0
        available_width = terminal_width - len(self.prefix + self.suffix) - self.percent_decimal - 10 - separator_length
        self.char_length = available_width//len(self.bars)

    @classmethod
    def create_bar(cls, total_iteration):
        return ProgressBar(total_iteration)

    def __str__(self):
        lock.acquire()  # Waiting the adding and updating bars
        lock.release()
        if len(self.bars) == 0:
            return ''
        average_percent = sum([bar.percent() for bar in self.bars])/len(self.bars)
        average_percent_in_string = ("{0:." + str(self.percent_decimal) + "f}").format(average_percent)
        bar = '|'.join([bar.encode_string(self.char_length) for bar in self.bars])
        return '\r%s |%s| %s%% %s' % (self.prefix, bar, average_percent_in_string, self.suffix)


class ProgressBar:
    def __init__(self, total_iteration):
        self.fill = '█'
        self.total_iteration = total_iteration
        self.current_iteration = 0

    def encode_string(self, char_length):
        filled_length = int(char_length * self.current_iteration // self.total_iteration)
        return self.fill * filled_length + '-' * (char_length - filled_length)

    def update(self, iteration):
        if iteration <= self.total_iteration:
            self.current_iteration = iteration

    def update_increment(self, iteration):
        self.current_iteration += iteration
        if self.current_iteration > self.total_iteration:
            self.current_iteration = self.total_iteration

    def percent(self):
        return (self.current_iteration/self.total_iteration) * 100
