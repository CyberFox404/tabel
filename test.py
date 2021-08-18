from lib.cycle_stepper import cycle_stepper

if __name__ == "__main__":
    cs = cycle_stepper(1, 3)

    for i in range(36):
        print("range %d" % i)
        print("check %d" % cs.check())
        cs.step()

        if (i+1) % 6 == 0 and i > 0:
            print("!!!")
            cs.nextgroup()

        print()

