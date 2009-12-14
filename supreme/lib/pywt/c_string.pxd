# Copyright (c) 2006-2009 Filip Wasilewski <http://filipwasilewski.pl/>
# See COPYING for license details.

# $Id: c_string.pxd 117 2009-05-02 20:25:59Z filipw $

cdef extern from "string.h":
	ctypedef long size_t
	void *memcpy(void *dst,void *src,size_t len)
	void *memmove(void *dst,void *src,size_t len)
	char *strdup(char *)
