def init():
    pass


def read_buffer():
    buffer = '[T:23, F:2, A:1]' '[T:1, F:43, A:16]' '[T:4, F:20, A:124]' '[T:13, F:54, A:23]'

    counter = 0
    buffer_i = 0

    while True:
        if counter > 100:
            counter += 1
            yield None
        elif counter > buffer_i:
            yield buffer[buffer_i % len(buffer)]
            buffer_i += 1
        else:
            yield None
            counter += 1
