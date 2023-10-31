from collections import OrderedDict

# Declare the set of choices and the values each choice can take.
aminos_list = ["A", "C", "D", "E", "F", "G", "H", "I", "K", "M", "N", "O" "P", "Q", "R", "S", "T", "U", "V", "W", "Y"]
aminos_list = ["A", "R", "N", "D", "B", "C", "E", "Q", "Z", "G", "H", "I", "L", "K", "M", "F", "P", "S", "T", "W", "Y", "V"]
SCHEMA = OrderedDict([(f"amino{i}", aminos_list) for i in range(4)])

# Declare some constraints. See pyroed.constraints for options.
CONSTRAINTS = []
#CONSTRAINTS.append(AllDifferent("amino0", "amino1", "amino2"))
#CONSTRAINTS.append(Iff(TakesValue("amino3", "T"), TakesValue("amino2", "T")))

# Specify groups of cross features for the Bayesian linear regression model.
FEATURE_BLOCKS = []
FEATURE_BLOCKS.append(["amino0"])  # single features
FEATURE_BLOCKS.append(["amino1"])
FEATURE_BLOCKS.append(["amino2"])
FEATURE_BLOCKS.append(["amino3"])
FEATURE_BLOCKS.append(["amino0", "amino1"])  # consecutive pairs
FEATURE_BLOCKS.append(["amino1", "amino2"])
FEATURE_BLOCKS.append(["amino2", "amino3"])

# Finally define Gibbs sampling blocks for the discrete optimization.
GIBBS_BLOCKS = []
GIBBS_BLOCKS.append(["amino0", "amino1"])  # consecutive pairs
GIBBS_BLOCKS.append(["amino1", "amino2"])
GIBBS_BLOCKS.append(["amino2", "amino3"])

