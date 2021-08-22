'''

from lib.cycle_stepper import cycle_stepper

cs = cycle_stepper(1, 3)

'''


class cycle_stepper:

    def __init__(self, min, group):
        self.min = min
        self.group = group
        self.current_step = min
        self.current_group = 1

    def step(self):
        self.current_step += 1
        if self.current_step > self.group * self.current_group + self.min - 1:
            self.current_step -= self.group + 0

    def nextgroup(self):
        self.current_group += 1
        self.current_step = self.group * self.current_group + self.min - self.group

    def check(self):
        return self.current_step


if __name__ == "__main__":
    st = cycle_stepper(0, 3)

    for i in range(36):
        print("range %d" % i)
        print("check %d" % st.check())
        st.step()

        if (i+1) % 6 == 0 and i > 0:
            print("!!!")
            st.nextgroup()

        print()