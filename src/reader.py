#!/usr/bin/python
"""

Reader for CSV files.
Reads head of CSV from file and manages it for the interface.

"""

import os
import sys
import logging


class Reader(object):

    def __init__(self, config):

        self.logger = logging.getLogger("Reader")

        # size of buffer to store in memory (in MB)
        self.buffer_size = config['buffer_size']
        # size of chunk of data -- number of lines
        self.chunk_size  = config['chunk_size']

        self.separator  = str(config['separator'])

        self.filename = config['filename']  # path to filename
        self.buffer = None                  # current buffer
        self.total_lines = 0                # number of lines in buffer
        self.current_line = 0               # current line in buffer

        self.__read_buffer()
        self.__validate_buffer()


    def __read_buffer(self):
        ''' read head of file into memory '''

        # filesize in Bytes
        file_size = os.path.getsize(self.filename)

        # Convert buffer size from MB to bytes
        buffer_size = self.buffer_size * (1024*1024)

        with open(self.filename, 'rU') as fid:
            if buffer_size > file_size:
                # if buffer size is too big, we just read the entire file
                lines = fid.readlines()
            else:
                # otherwise, we read the top buffer size
                data = fid.read(buffer_size)
                lines = data.split('\n')
                # and we discard the last trailing line
                if data[-1] != '\n':
                    lines.pop()

        self.buffer = lines
        self.total_lines = len(self.buffer)
        self.file_size   = round(file_size/(1024*1024.), 2)

        # update chunk size, if too big
        if self.chunk_size > self.total_lines:
            self.chunk_size = self.total_lines

        self.logger.info('Loaded {0} lines to buffer'.format(self.total_lines))
        self.logger.info('Buffer size: {0} MB, File size {1} MB'.format(self.buffer_size, self.file_size))


    def __validate_buffer(self):
        ''' make sure all lines have the same number of columns '''
        separator = self.separator

        first_line = self.buffer[0]
        n_cols = len( first_line.rstrip().split(self.separator) )

        for i, line in enumerate(self.buffer):
             cols = len( line.rstrip().split(self.separator))

             if cols != n_cols:
                self.logger.critical('Mismatch number of columns at line {0}'.format(i))
                sys.exit(1)


    def next(self):
        ''' Read next chunk of the buffer.
            If we are at the end, we just return the last chunk
        '''
        current_position = self.current_line
        total_lines = self.total_lines
        chunk_size  = self.chunk_size

        start = current_position
        if current_position == total_lines:
            start = current_position - chunk_size

        end = start + chunk_size
        if end > total_lines:
            end = total_lines

        self.current_line = end

        return self.buffer[start:end]

    def previous(self):
        ''' Read previous chunk of the buffer.
            If we are at the beginning, we just return the first chunk
        '''
        current_position = self.current_line
        chunk_size  = self.chunk_size

        start = current_position - chunk_size
        if current_position < 0:
            start = 0

        end = start + chunk_size
        self.current_line = end
        return self.buffer[start:end]


