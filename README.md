# Projektni zadatak broj 4, Genomska Informatika, skolska 2021/2022

## Aleksandar Malovic 2021/3375

Video presentation: [Video presentation](https://www.youtube.com/watch?v=hhbMQNiOfj0)

### Repository structure:

#### Helpers
helper.py - Helper functions  
helper_tests.py - Helper functions unit tests

#### Burrows-Wheeler transform
bwt_unoptimised.py - Initial unoptimised implementation of BWT  
bwt_unoptimised_tests.py - Unit tests of initial BWT implementation  
bwt_optimised_sp.py - Single process optimisation of BWT  
bwt_optimised_sp_tests.py - Unit tests of single process optimisation of BWT

#### Burrows-Wheeler transform with multiprocessing (WIP)
shared_memory_management.py - shared memory helpers  
bwt_optimised_sort.py - Multiprocess multi-key quicksort implementation  
bwt_optimised.py - BWT calculation with mp mkquicksort  
bwt_optimised_tests.py - Unit tests of multiprocess BWT calculation  

#### FM index
fmi_unoptimised.py - unoptimised FM index structures  
fmi_unoptimsed_structure_tests.py - unit tests of unoptimised FM index structures  
fmi_optimised_sp.py - single process optimised FM index structures  
fmi_optimsed_sp_structure_tests.py - unit tests of single process optimised FM index structures  

#### FM index with multiprocessing (WIP)
fmi_optimised.py - miltiprocess optimised FM index structures  
fmi_optimsed_structure_tests.py - unit tests of multiprocess optimised FM index structures

#### FM index functionality testing
fmi_shared_functionality_tests.py - shared tests for all implementations of functionality of FM index structures and FM index itself  
All structures are subjected to the same functionality tests to ensure no regressions between implementations. All implementations of FM index are also subjected to the same tests to ensure all implementations return the same results.

#### Combined testing
unit_test.py - runs all defined tests for all implementations

#### Performance testing
unoptimised_performance_test.py - performance test of initial unoptimised implementation  
sp_optimised_performance_test.py - performance test of single process optimised implementation  
optimised_performance_test.py - performance test of multiprocess optimised implementation

