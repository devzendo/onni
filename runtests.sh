#!/bin/bash
# To be run after buildtests has set the tree up for tests.
(cd build && make && make test)

