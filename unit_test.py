from bwt_optimised_sp_tests import testSpBWTOptimised
from fmi_optimised_sp_structure_tests import testSpOptimisedFMIStructures
from helper_tests import testHelpers
from bwt_unoptimised_tests import testBWTUnoptimised
from fmi_unoptimised_structure_tests import testUnoptimisedFMIStructures
from fmi_optimised_structure_tests import testOptimisedFMIStructures
from fmi_shared_functionality_tests import testSpOptimisedFMIndex, testUnoptimisedFMIndex, testOptimisedFMIndex
from bwt_optimised_tests import testBwtOptimised

if __name__ == '__main__':
    testHelpers()
    print('Helper unit tests passed!')
    testBWTUnoptimised()
    print('BWT unoptimised unit tests passed!')
    testSpBWTOptimised()
    print('BWT sp optimised unit tests passed!')
    testBwtOptimised()
    print('BWT optimised unit tests passed!')
    testUnoptimisedFMIStructures()
    print('Unoptimised structures unit tests passed!')
    testUnoptimisedFMIndex()
    print('Unoptimised FMI unit tests passed!')
    testSpOptimisedFMIStructures()
    print('Sp optimised structures unit tests passed!')
    testSpOptimisedFMIndex()
    print('Sp optimised FMI unit tests passed!')
    testOptimisedFMIStructures()
    print('Optimised structures unit tests passed!')
    testOptimisedFMIndex()
    print('Optimised FMI unit tests passed!')

    print('ALL UNIT TESTS PASSED!!!')