'''
 rmtoo
   Free and Open Source Requirements Management Tool
   
  Generic Iterator
   
 (c) 2012 by flonatel GmbH & Co. KG

 For licensing details see COPYING
'''

class GenIterator:
    '''Generic iterator: adds a current to the standard container 
       iterators.'''

    def __init__(self, iterator):
        '''Initialize the iterator.'''
        self.__iterator = iterator
        self._current = None
        self._next()

    def _next(self):
        '''Iterates to the next element.'''
        try:
            self._current = self.__iterator.next()
        except StopIteration:
            return None
        return self._current

    def _get_current(self):
        '''Returns the current element.'''
        return self._current
    
    def next(self):
        return self._next()
    
    def current(self):
        return self._current