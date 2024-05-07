import time

import psutil

import interface


def notepad_started():
    for process in psutil.process_iter(['pid', 'name']):
        try:
            if process.name() == 'notepad.exe':
                return True
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
    return False


def main():
    # gui = interface.App()
    # gui.mainloop()

    started = False
    start_time = None

    while True:
        if notepad_started():
            if not started:
                start_time = time.time()
                started = True
                print('Notepad started')
            else:
                print('Notepad is running')
        else:
            if started:
                started = False
                print(f'Notepad was running for {int(time.time() - start_time)} seconds')
        time.sleep(1)


if __name__ == "__main__":
    main()
