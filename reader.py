#!/usr/bin/python
"""
The purpose of this is to write a reader for large files.
The reader should return n lines in chunks and it should
be able to traverse the file back and forward.

Example: initially return the first 1000 lines.
Then return the next 1000 lines (1001-2000).
It then has the option of returning (1-1000) or (2001-3000).

This should be done without loading the entire file into memory.

"""

import os
import sys



"""
Two key concepts:

_Buffer: This is a segment of the file that is kept in memory. We traverse this buffer
         and we return chunks of data.

_Chunk: This is what the Reader returns. It navigates through the Buffer back and forth
        and returns chunks of data. Chunk is defined in terms of lines.

Methods:
_Next(): Navigate through Buffer and return next Chunk.
_Previous(): Navigate through Buffer and return previous Chunk.

If we the next or previous Chunk is beyond the Buffer boundary, we need to re-define the buffer
by reading from the file and discarding data at the other edge.

Ideally, the Chunk would be approximately around the middle of the Buffer.
We could define a threshold, say the 1st and 3rd Quartile. If we reach those, we redefine the buffer
such that the new position is at the middle of the new buffer.


Example:
......................|-------------|+++++++|----------|......................
 file-not-in-memory       buffer      chunk    buffer      file-not-in-memory


"""


class Reader(object):

    def __init__(self, filename):

        self.chunk_size  = 1000             # size to chunks of data to return (number of lines)
        self.buffer_size = 1                # size of buffer to store in memory (in MB)

        self.filename = filename            # path to filename
        self.handle = open(filename, 'rU')  # file handle, keep file open

        self.buffer = None                  # current buffer

        self.trailing_line  = None          # if buffer cuts a line in the middle
        self.trailing_buffer = []           # remaining lines from buffer according to chunk size

        self.position = 0                   # current position in terms of lines in file
        self.filesize = None                # total filesize
        self.remaining_size = None          #

        self.buffer_info = {}
        self.current_buffer = 0

        self.previous_direction = 1

        # convert buffer size from MB to bytes
        self.buffer_size = self.buffer_size * (1024*1024)

        # find total file size
        self.handle.seek(0, os.SEEK_END)
        self.filesize = self.handle.tell()
        self.remaining_size = self.filesize
        self.handle.seek(0, os.SEEK_SET)

        self.ReadNextBuffer()


    def PrintState(self):
        #print '    chunk-size', self.chunk_size
        #print '    buffer-size', self.buffer_size
        #print '    filesize', self.filesize
        print '    position', self.position
        print '    buffer length', len(self.buffer)


    def ReadNextBuffer(self):
        """ Read Next Forward """

        ## Clear current buffer here???
        # Do this to avoid having two buffers in memory

        print '    read buffer forward'

        self.current_buffer += 1

        print '    loading buffer', self.current_buffer

        data = self.handle.read(self.buffer_size)
        lines = data.split('\n')

        self.remaining_size = self.filesize - self.buffer_size

        if self.remaining_size < 0:
            self.remaining_size = 0

        # add trailing lines from previous buffer
        if self.trailing_line:
            lines[0] = self.trailing_line + lines[0]

        # remove trailing lines from current buffer
        if data[-1] != '\n' and self.remaining_size > 0:
            self.trailing_line = lines.pop()
        else:
            self.trailing_line = None

        self.buffer = self.trailing_buffer + lines

        if self.remaining_size > 0:
            leftover = len(self.buffer) % self.chunk_size
            bufflines = len(self.buffer) - leftover

            self.trailing_buffer = self.buffer[bufflines:]
            self.buffer = self.buffer[:bufflines]

        if self.current_buffer not in self.buffer_info:
            self.buffer_info[self.current_buffer] = len(self.buffer)

        self.position = 0


    def ReadPreviousBuffer(self):
        """ TODO: read buffer backward """

        ### Need to reconstruct previous buffer by reading
        ### Two blocks from the file
        # We need to find the trailing buffer/lines from the previous buffer

        print '    read buffer BACKWARD'

        self.current_buffer -= 1
        print '    loading buffer', self.current_buffer

        current_position = self.handle.tell()

        # find trailing buffer from previous buffer
        backward_position = max(0, current_position - (self.buffer_size*3))
        print 'backward position', backward_position

        if self.current_buffer > 1: 
            self.handle.seek(backward_position)
            data = self.handle.read(self.buffer_size)
            lines = data.split('\n')

            # remove trailing lines from current buffer
            if data[-1] != '\n':
                trailing_line = lines.pop()
            else:
                trailing_line = None

            # remove extra lines at the end
            n_lines = self.buffer_info[self.current_buffer-1]
            leftover = n_lines % self.chunk_size
            bufflines = n_lines - leftover
            trailing_buffer = self.buffer[bufflines:]

        else: # beginning of file
            trailing_line = None
            trailing_buffer = []

        backward_position = max(0, current_position - (self.buffer_size*2))
        self.handle.seek(backward_position)
        data = self.handle.read(self.buffer_size)
        self.remaining_size += self.buffer_size
        lines = data.split('\n')

         # add trailing lines from previous buffer
        if trailing_line:
            lines[0] = trailing_line + lines[0]

        if data[-1] != '\n':
            lines.pop()

        self.buffer = trailing_buffer + lines

        # remove extra lines at the end
        leftover = len(self.buffer) % self.chunk_size
        bufflines = len(self.buffer) - leftover
        self.buffer = self.buffer[:bufflines]

        self.position = len(self.buffer)
        print self.buffer_info[self.current_buffer], len(self.buffer)




    def Next(self):
        """ Move chunk forwards along buffer """

        if self.previous_direction == -1:
            self.position += self.chunk_size

        end_position = self.position + self.chunk_size


        self.PrintState()
        print '    end position', end_position

        if end_position > len(self.buffer):
            # either need to move buffer or we are at the end of file
            if self.remaining_size <= 0:
                end_position = len(self.buffer)
            else:
                self.ReadNextBuffer()
                end_position = self.position + self.chunk_size

        chunk = self.buffer[self.position:end_position]
        print '    visualize %i:%i' % (self.position, end_position)
        self.position = end_position
        self.previous_direction = 1
        return chunk


    def Previous(self):
        """ Move chunk backwards along buffer 
            TODO: need to update to include Read Backward Buffer """

        if self.previous_direction == 1:
            self.position -= self.chunk_size

        end_position = self.position - self.chunk_size

        self.PrintState()
        print '    end position', end_position

        print '    rem size', self.remaining_size, self.filesize

        if end_position < 0:
            # either need to move buffer backwards or we are at the beginning of file
            if self.current_buffer == 1:
                end_position = 0
            else:
                self.ReadPreviousBuffer()
                end_position = self.position - self.chunk_size
 
        chunk = self.buffer[end_position:self.position]
        print '    visualize %i:%i' % (end_position, self.position)
        self.position = end_position
        self.previous_direction = -1

        return chunk




def main(filename):

    # this function for testing/debugging purposes only -- to be removed
    import fileinput
    truth = [line.rstrip() for line in fileinput.input(filename)]
    
    #import random

    rd = Reader(filename)

    """
    for i in range(10000):
        direction = random.random()
        if direction > 0.5:
            print 'start FORWARD CALL', i+1
            chunk = rd.Next()
        else:
            print 'start BACKWARD CALL', i+1
            chunk = rd.Previous()
    print '    after -> position:', rd.position, len(chunk)
    """

    """
    data = []
    for i in range(50):
        data.extend(rd.Next())

    for i in range(len(data)):
        if data[i] != truth[i]:
            print i
    """


    ### Current issues:
    # Trailing lines when reading buffers backwards
    # Works well at the end edge, but not all the way to the beginning


    #offset = 0
    #file_size = fh.seek(0, os.SEEK_END)
    #total_size = remaining_size = fh.tell()

    #print file_size
    #print total_size



#if __name__ == "__main__":
    #filename = ''
    #main(filename)

