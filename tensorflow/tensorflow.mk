# Makefile for tensorflow plugin for MLDB

# Tensorflow plugins
LIBMLDB_TENSORFLOW_PLUGIN_SOURCES:= \
	tensorflow_plugin.cc \

#	test.cu.cc

$(eval $(call set_compile_option,$(LIBMLDB_TENSORFLOW_PLUGIN_SOURCES),$(TENSORFLOW_COMPILE_FLAGS) -Imldb/ext/tensorflow))

# Make these depend upon Tensorflow's version of the protobuf compiler
# since the headers that they need are installed with it.
#
# They also need access to the generated tensorflow headers
$(LIBMLDB_TENSORFLOW_PLUGIN_SOURCES:%=$(CWD)/%): $(HOSTBIN)/protoc $(DEPENDS_ON_TENSORFLOW_HEADERS)

$(eval $(call mldb_plugin_library,tensorflow,mldb_tensorflow_plugin,$(LIBMLDB_TENSORFLOW_PLUGIN_SOURCES),tensorflow-cpp-interface))

$(eval $(call mldb_builtin_plugin,tensorflow,mldb_tensorflow_plugin,doc))

$(eval $(call mldb_unit_test,MLDB-1203-tensorflow-plugin.js,tensorflow,manual))

#$(eval $(call include_sub_make,pro_testing,testing,pro_testing.mk))
