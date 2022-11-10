CC := gcc
CFLAGS := -Wall

BUILDDIR := ./build
LIBDIR := ./lib
TESTDIR := ./test

MODULES_C := $(shell find $(LIBDIR) -name *.c)
MODULES_H := $(shell find $(LIBDIR) -name *.h)
MOD_OBJS := $(notdir $(MODULES_C)) 
MOD_OBJS := $(MOD_OBJS:%.c=$(BUILDDIR)/%.o)

# OS detection
OS_NAME = Windows
ifeq ($(OS), Windows_NT)
	MOD_OBJS += lib/buffer/windows.o
else
	UNAME = $(shell uname -s)
	ifeq ($(UNAME), Linux)
		OS_NAME = Linux
		MOD_OBJS += lib/buffer/linux.o
	else
		OS_NAME = Unknown
		MOD_OBJS += lib/buffer/macos.o
	endif
endif

TESTS := $(shell find $(TESTDIR) -name *.c)
TEST_OBJS := $(notdir $(TESTS)) 
TEST_OBJS := $(TEST_OBJS:%.c=$(BUILDDIR)/%.o)
TEST_FILES  := $(notdir $(TESTS))
TEST_EXE := $(TEST_FILES:%.c=%.exe)
TEST_FILES := $(TEST_FILES:%.c=$(BUILDDIR)/%.exe)

INC_DIRS := $(shell find $(LIBDIR) -type d)
INC_FLAGS := $(addprefix -I,$(INC_DIRS))
VPATH := $(INC_DIRS)


all: clean mkbuild $(TEST_FILES)
	@echo "Built on $(OS_NAME)"

test: clean mkbuild $(TEST_FILES) run_test

run_test: $(TEST_EXE)

$(TEST_EXE):
	$(BUILDDIR)/$@

$(BUILDDIR)/%.exe: $(BUILDDIR)/%.o $(MOD_OBJS)
	$(CC) -o $@ $^

$(BUILDDIR)/%.o: $(TESTDIR)/%.c $(MODULES_H) 
	$(CC) $(CFLAGS) -MMD -c $< $(INC_FLAGS) -o $@

$(BUILDDIR)/%.o: %.c %.h 
	$(CC) $(CFLAGS) -MMD -c $< $(INC_FLAGS) -o $@


.PHONY: clean all test mkbuild run_test

clean:
	@rm -rf $(BUILDDIR)

mkbuild:
	mkdir -p $(BUILDDIR)