# sql_testing.mk
# Jeremy Barnes, 10 April 2016
# This file is part of MLDB. Copyright 2015 Datacratic. All rights reserved.

$(eval $(call test,path_test,sql_expression,boost))
