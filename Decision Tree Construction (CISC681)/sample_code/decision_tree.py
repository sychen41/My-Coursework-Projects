import math,operator,re,random,copy
from collections import defaultdict, Counter
# A small portion of the following code is modified from https://github.com/gumption/Python_for_Data_Science/blob/master/4_Python_Simple_Decision_Tree.ipynb

# load data to list of instances. one instance per line
def load_instances(filename):
    instances = []
    fileR = open(filename, "r")
    for line in fileR:
        new_instance = line.strip().split(',')
        instances.append(new_instance)
    fileR.close()
    return instances

# read attribute names from a txt file
def get_attribute_names(att_name_file_path):
    att_names = []
    fileR = open(att_name_file_path, "r")
    for line in fileR.read().splitlines():
        att_names.append(line)
    fileR.close()
    #print(att_names)
    return att_names

# get all values for an attribute given the index of the it
# return a set (no duplicated value)
def attribute_values(instances, attribute_index):
    return list(set([x[attribute_index] for x in instances]))

# get all values for an attribute given the index of the it
# return a list
def attribute_values_list(instances, attribute_index):
    return list(([x[attribute_index] for x in instances]))

# calculate the entropy for a given attribute
def entropy(instances, class_index=-1, attribute_name=None, value_name=None):
    num_instances = len(instances)
    if num_instances <= 1:
        return 0
    value_counts = defaultdict(int)
    for instance in instances:
        value_counts[instance[class_index]] += 1
    num_values = len(value_counts)
    if num_values <= 1:
        return 0
    attribute_entropy = 0.0
    if attribute_name:
        print('entropy({}{}) = '.format(attribute_name, 
        	'={}'.format(value_name) if value_name else ''))
    for value in value_counts:
        value_probability = value_counts[value] / num_instances
        child_entropy = value_probability * math.log(value_probability, num_values)
        attribute_entropy -= child_entropy
        if attribute_name:
            print('  - p({0}) x log(p({0}), {1})  =  - {2:5.3f} x log({2:5.3f})  =  {3:5.3f}'.format(
                value, num_values, value_probability, child_entropy))
    if attribute_name:
        print('  = {:5.3f}'.format(attribute_entropy))
    return attribute_entropy

# calculate the information gain for splitting on an attribute
def information_gain(instances, parent_index, class_index=0, attribute_name=False):
    parent_entropy = entropy(instances, class_index, attribute_name)
    child_instances = defaultdict(list)
    for instance in instances:
        child_instances[instance[parent_index]].append(instance)
    children_entropy = 0.0
    num_instances = len(instances)
    for child_value in child_instances:
        child_probability = len(child_instances[child_value]) / num_instances
        children_entropy += child_probability * entropy(
        	child_instances[child_value], class_index, attribute_name, child_value)
    return parent_entropy - children_entropy

# decide the majority class value given a bunch of instances
def majority_value(instances, class_index=0):
    class_counts = Counter([instance[class_index] for instance in instances])
    return class_counts.most_common(1)[0][0]

# find the attribute (index) that gives the most information gain
def choose_best_attribute_index(instances, candidate_attribute_indexes, class_index=0):
    gains_and_indexes = sorted([(information_gain(instances, i), i) for i in candidate_attribute_indexes],
                               reverse=True)
    return gains_and_indexes[0][1]

# return a dict type of subset of instances after splitting on the attribute.
# key: each value of this attribute
# value: subset of instances that have the value of the attribute equal to the key
def split_instances(instances, attribute_index):
    partitions = defaultdict(list)
    for instance in instances:
        partitions[instance[attribute_index]].append(instance)
    return partitions

# create DT recursively based on always choosing the attribut that has the most information gain.
def create_decision_tree(instances, candidate_attribute_indexes=None, class_index=0, default_class=None, prune=0,trace=0):

    # if no candidate_attribute_indexes are provided, assume that we will use all but the target_attribute_index
    if class_index == -1:
        class_index = len(instances[0])-1
    if candidate_attribute_indexes is None:
        candidate_attribute_indexes = [i for i in range(len(instances[0])) if i != class_index]
        #candidate_attribute_indexes.remove(class_index)
        
    class_labels_and_counts = Counter([instance[class_index] for instance in instances])

    # if we do pre-prune
    if prune > 0 and len(instances) < prune:
        if trace:
            print('{}Using default class because of pruning{}'.format('< ' * trace, default_class))
        return default_class

    # If the dataset is empty or the candidate attributes list is empty, return the default value
    if not instances or not candidate_attribute_indexes:# or len(instances) < prune:
        if trace:
            print('{}Using default class {}'.format('< ' * trace, default_class))
        return default_class


    # If all the instances have the same class label, return that class label
    elif len(class_labels_and_counts) == 1:
        class_label = class_labels_and_counts.most_common(1)[0][0]
        if trace:
            print('{}All {} instances have label {}'.format('< ' * trace,
            	len(instances), class_label))
        return class_label
    else:
        default_class = majority_value(instances, class_index)

        # Choose the next best attribute index to best classify the instances
        best_index = choose_best_attribute_index(instances, candidate_attribute_indexes, class_index)
        if trace:
            print('{}Creating tree node for attribute index {}'.format('> ' * trace, best_index))

        # Create a new decision tree node with the best attribute index and an empty dictionary object (for now)
        tree = {best_index:{}}

        # Create a new decision tree sub-node (branch) for each of the values in the best attribute field
        partitions = split_instances(instances, best_index)

        # Remove that attribute from the set of candidates for further splits
        remaining_candidate_attribute_indexes = [i for i in candidate_attribute_indexes if i != best_index]
        for attribute_value in partitions:
            if trace:
                print('{}Creating subtree for value {} ({}, {}, {}, {})'.format(
                    '> ' * trace,
                    attribute_value,
                    len(partitions[attribute_value]),
                    len(remaining_candidate_attribute_indexes),
                    class_index,
                    default_class))

            # Create a subtree for each value of the the best attribute
            subtree = create_decision_tree(
                partitions[attribute_value],
                remaining_candidate_attribute_indexes,
                class_index,
                default_class,
                prune,
                trace + 1 if trace else 0)

            # Add the new subtree to the empty dictionary object in the new tree/node we just created
            tree[best_index][attribute_value] = subtree

    return tree

# use the DT to predict the class value of an instance.
def classify(tree, instance, default_class=None):
    if not tree:
        return default_class
    if not isinstance(tree, dict): 
        return tree
    attribute_index = list(tree.keys())[0]  # using list(dict.keys()) for Python 3 compatibiity
    attribute_values = list(tree.values())[0]
    instance_attribute_value = instance[attribute_index]
    if instance_attribute_value not in attribute_values:
        return default_class
    return classify(attribute_values[instance_attribute_value], instance, default_class)

# compute the accracy
def classification_accuracy(tree, testing_instances, class_index=0):
    num_correct = 0
    for i in range(len(testing_instances)):
        prediction = classify(tree, testing_instances[i])
        actual_value = testing_instances[i][class_index]
        if prediction == actual_value:
            num_correct += 1
    return num_correct / len(testing_instances)

# compute the recall
def classification_recall(tree, testing_instances, class_index=0):
    recall_for_each_class = {}
    for i in range(len(testing_instances)):
        actual_value = testing_instances[i][class_index]
        if actual_value not in recall_for_each_class:
            recall_for_each_class[actual_value] = [1,0]
        else:
            recall_for_each_class[actual_value][0] += 1

    for i in range(len(testing_instances)):
        prediction = classify(tree, testing_instances[i])
        actual_value = testing_instances[i][class_index]
        if prediction == actual_value:
            recall_for_each_class[actual_value][1] += 1
    num_of_classes = len(recall_for_each_class)
    recall = 0
    for key, value in recall_for_each_class.items():
        recall += value[1]/value[0]
    recall = recall/num_of_classes
    return recall

treeInfo = []
unique_index = 0
level_of_tree = []
# recursively walk through the tree
def walk_a_tree(tree,level,att,value):
    global unique_index
    while bool(tree):
        pair = tree.popitem()
        #print(pair)
        if type(pair) is tuple:
            string = ""
            if type(pair[0]) is int:
                #print(level)
                level+=1
                #print("lvl: " + str(level))
                level_of_tree.append(level)
                #string = "att " + str(pair[0])
                #new_att = "att-" + str(pair[0]) + " v-" + value + " l-" + str(level)
                new_att = "att " + str(pair[0]) + " v" + value + "l" + str(level)
                att = new_att + "|" + att
                #new_att_flag = True
            else:
                #temp = "att " + att + " l " + str(level)
                #print(att)
                treeInfo.append(att)
                #string = "value " + str(pair[0])
                string = str(pair[0]) # value of attribute
                unique_index+=1
                value = str(pair[0])
                #print(string)
                #print(string + " u" + str(unique_index))
                treeInfo.append(string)
            if isinstance(pair[1], str):
                #print("level: " + str(level))
                #string = "class " + str(pair[1])
                string = str(pair[1]) + "_u" + str(unique_index) # class value
                #print(string)
                treeInfo.append(string)
            else:
                walk_a_tree(pair[1],level,att,value)
                #level-=1

# convert the DT to a tgf file
def format_a_tree_to_a_tgf_file(tree, att_name_file_path,final_tree_tgf_file_path):
    # firstly, through walking the tree recursively, get information of every edge(node-value-node) of the tree
    walk_a_tree(tree,0,"","X")
    # secondly, format the output appropriately.
    att_in_tree = []
    pattern = re.compile("att")
    for item in treeInfo:
        if pattern.match(item):
            #att_in_tree[int(item.split("att")[-1])] = {}
            if item not in att_in_tree:
                att_in_tree.append(item)

    att_names = get_attribute_names(att_name_file_path)

    att_index_to_name_map = {}
    unique_suffix = 0
    att_in_tree_real_name = []
    for att in att_in_tree:
        unique_att_name = att_names[int(att.split(" ")[1])] + "_" + str(unique_suffix)
        att_index_to_name_map[att] = unique_att_name
        att_in_tree_real_name.append(unique_att_name)
        unique_suffix+=1

    new_tree_info = []
    for item in treeInfo:
        if pattern.match(item):
            new_tree_info.append(item)
        new_tree_info.append(item)

    new_tree_info_with_real_name = []
    for item in new_tree_info:
        if pattern.match(item):
            new_tree_info_with_real_name.append(att_index_to_name_map[item])
        else:
            new_tree_info_with_real_name.append(item)

    final_tree_info = []
    start = ""
    value = ""
    end = ""
    while new_tree_info_with_real_name:
        first = new_tree_info_with_real_name.pop(0)
        second = new_tree_info_with_real_name.pop(0)
        if first == second:
            start = str(first)
            value = str(new_tree_info_with_real_name.pop(0))
            end = str(new_tree_info_with_real_name.pop(0))
        else:
            start = str(first)
            value = str(second)
            end = str(new_tree_info_with_real_name.pop(0))
        if end in att_in_tree_real_name:
            edge = str(att_in_tree_real_name.index(start))+ " " + str(att_in_tree_real_name.index(end))+ " " + value
        else:
            edge = str(att_in_tree_real_name.index(start))+ " " + end + " " + value
        final_tree_info.append(edge)

    output_format = []
    for x in range(len(att_in_tree_real_name)):
        output_format.append(str(x) + " " + att_in_tree_real_name[x])
    output_format.append("#")
    for edge in final_tree_info:
        output_format.append(edge)
    fileW = open(final_tree_tgf_file_path, "w")
    for line in output_format:
        fileW.write(line)
        fileW.write("\n")
    fileW.close()
    print("The DT tree information:")
    print("max depth: " + str(max(level_of_tree)+1))
    print("number of node: " + str(unique_index+1))
    print("Tree graph: please open the tgf file that just generated.")

# first type of dicretization: fixed frequency: every interval has the same number of instances.
def fix_frequency_discretization(instances,continuous_att_index_list,discretized_data_path,nominal_att_index=-1):
    # number of bins = squre root of total number of instances
    num_bins = int(math.sqrt(len(instances)))
    new_data_map = {}
    for att_index in continuous_att_index_list:
        att_index_value_map = {}
        index = 0
        att_values = attribute_values_list(instances, att_index)
        for value in att_values:
            att_index_value_map[index] = value
            index+=1
        #print(att_index_value_map)
        sorted_map = sorted(att_index_value_map.items(), key=operator.itemgetter(1))
        #print(sorted_map)
        new_map = {}
        count = 0
        bin_value = 1
        split_point = num_bins
        for pair in sorted_map:
            if count < split_point:
                new_map[pair[0]] = bin_value
            else:
                split_point+=num_bins
                bin_value+=1
                new_map[pair[0]] = bin_value
            count+=1
        sorted_new_map = sorted(new_map.items(), key=operator.itemgetter(0))
        #print(sorted_new_map)
        discretized_value = []
        for pair in sorted_new_map:
            discretized_value.append(pair[1])
        #print(discretized_value)
        new_data_map[att_index] = discretized_value
    data_after_discretization = []
    #print(new_data_map)
    # change nominal attribute value to numbers. for instance, Europe => 1, America => 2, etc
    all_nominal_values = []
    if nominal_att_index != -1:
        all_nominal_values = attribute_values(instances, nominal_att_index)
        print("changing nominal values to numeric values:")
        for nominal_value in all_nominal_values:
            print(nominal_value + " => " + str(all_nominal_values.index(nominal_value)+1))
    fileW = open(discretized_data_path,"w")
    for y in range(len(instances)):
        instance = instances[y]
        temp_string = ""
        for x in range(len(instance)):
            if x not in new_data_map:
                if nominal_att_index != -1 and x == nominal_att_index:
                    temp_string += str(all_nominal_values.index(instance[x])+1)
                else:
                    temp_string += str(instance[x])
            else:
                temp_string += str(new_data_map[x][y])
            if x != len(instance)-1:
                temp_string += ","
        data_after_discretization.append(temp_string)
        fileW.write(temp_string + "\n")
    fileW.close()

# second type of dicretization: fixed inteval: every interval has the same range. i.e., (11-15),(16-20)...
# the first inteval always starts from 0, and the last interval always ends with infinite (use 999999999 instead).
def fix_interval_discretization(instances,continuous_att_index_list,discretized_data_path,nominal_att_index=-1):
    # number of bins = squre root of total number of instances
    num_bins = int(math.sqrt(len(instances)))
    num_intervals = num_bins + 1
    new_data_map = {}
    for att_index in continuous_att_index_list:
        att_index_value_map = {}
        index = 0
        att_values = []
        for v in attribute_values_list(instances, att_index):
            att_values.append(float(v))
        #print(att_values)
        min_value = min(att_values)
        max_value = max(att_values)
        interval_step = int((max_value-min_value+1)/num_intervals)
        interval_point= min_value
        interval_points = []
        for k in range(num_bins):
            interval_point += interval_step
            interval_points.append(interval_point)
        #print(interval_points)
        range_pairs = []
        for k in range(num_bins):
            if k == 0:
                range_pairs.append((0,interval_points[0]))
                range_pairs.append((interval_points[k],interval_points[k+1]))
            elif k == num_bins-1:
                range_pairs.append((interval_points[k],999999999))
            else:
                range_pairs.append((interval_points[k],interval_points[k+1]))
        # uncomment next line if you want to see what intervals are
        #print(range_pairs)
        for value in att_values:
            att_index_value_map[index] = value
            index+=1
        #print(att_index_value_map)
        new_map = {}
        for key, value in att_index_value_map.items():
            for l in range(len(range_pairs)):
                if range_pairs[l][0] <= value < range_pairs[l][1]:
                    new_map[key] = l+1
                    continue
        #print(new_map)
        sorted_new_map = sorted(new_map.items(), key=operator.itemgetter(0))
        #print(sorted_new_map)
        discretized_value = []
        for pair in sorted_new_map:
            discretized_value.append(pair[1])
        #print(discretized_value)
        new_data_map[att_index] = discretized_value
    data_after_discretization = []
    #print(new_data_map)
   # change nominal attribute value to numbers. for instance, Europe => 1, America => 2, etc
    all_nominal_values = []
    if nominal_att_index != -1:
        all_nominal_values = attribute_values(instances, nominal_att_index)
        print("changing nominal values to numeric values:")
        for nominal_value in all_nominal_values:
            print(nominal_value + " => " + str(all_nominal_values.index(nominal_value)+1))
    fileW = open(discretized_data_path,"w")
    for y in range(len(instances)):
        instance = instances[y]
        temp_string = ""
        for x in range(len(instance)):
            if x not in new_data_map:
                if nominal_att_index != -1 and x == nominal_att_index:
                    temp_string += str(all_nominal_values.index(instance[x])+1)
                else:
                    temp_string += str(instance[x])
            else:
                temp_string += str(new_data_map[x][y])
            if x != len(instance)-1:
                temp_string += ","
        data_after_discretization.append(temp_string)
        fileW.write(temp_string + "\n")
    fileW.close()

###########################################################################################
# Here start the MAIN
#Define your folder path
folder_path = "C:\\Users\\Shiyi\\Google Drive\\courses\\681 AI\\DTproject_AI\\sample_code\\"
#part3 = True #if False, then run part2
part3 = False
if part3:
    # for part3
    print("PART 3:")
    training_data_filename = "wdbc-train.data"
    testing_data_filename = "wdbc-test.data"

    training_instances = load_instances(training_data_filename)
    testing_instances = load_instances(testing_data_filename)
    print("Training data " +  training_data_filename + " contains " + str(len(training_instances)) + ' instances')
    # if prune > 0, than pre-pruning if the number of instances is less than prune
    # if prune = 0, than no pre-pruning
    pre_prune_threshold = 0
    if pre_prune_threshold == 0:
        print("No pre pruning")
    else:
        print("Pre pruning with threshold set at " + str(pre_prune_threshold))
    tree = create_decision_tree(training_instances,trace=0,prune=pre_prune_threshold,class_index=-1)
    tree_copy = copy.deepcopy(tree)
    attribute_name_file_path = folder_path + "wdbc-att-names.txt"
    final_tree_tgf_file_path = folder_path + "tree_part3.tgf"
    format_a_tree_to_a_tgf_file(tree,attribute_name_file_path,final_tree_tgf_file_path)
    print("accuracy on training data:: " + str(classification_accuracy(tree_copy,training_instances,-1)))
    print("accuracy on testing data:: " + str(classification_accuracy(tree_copy,testing_instances,-1)))
    print("recall on training data: " + str(classification_recall(tree_copy,training_instances,-1)))
    print("recall on testing data: " + str(classification_recall(tree_copy,testing_instances,-1)))
    # end for part3
else:
    # for part2
    # for files that need discretization
    print("PART 2:")
    undiscretized_data_filename = folder_path + "mpg_cars.txt"
    discretization_type = "f"
    instances = load_instances(undiscretized_data_filename)
    discretized_data_path = folder_path + "discretized_data.txt"
    if discretization_type == "f":
        print("discretization method: fixed frequency")
        fix_frequency_discretization(instances,[2,3,4,5],discretized_data_path,7)
    else:
        print("discretization method: fixed interval")
        fix_interval_discretization(instances,[2,3,4,5],discretized_data_path,7)
    # now we load discretized data
    data_filename = folder_path + "discretized_data.txt"
    all_instances = load_instances(data_filename)
    num_instances = len(all_instances)
    ten_percent = int(num_instances*0.1)
    random_list = random.sample(range(0,len(all_instances)),ten_percent)
    training_instances = []
    testing_instances = []
    for m in range(num_instances):
        if m in random_list:
            testing_instances.append(all_instances[m])
        else:
            training_instances.append(all_instances[m])

    print("Training data" +  " contains " + str(len(training_instances)) + ' instances')
    print("Testing data" +  " contains " + str(len(testing_instances)) + ' instances')
    # if prune > 0, than pre-pruning if the number of instances is less than prune
    # if prune = 0, than no pre-pruning
    pre_prune_threshold = 0
    if pre_prune_threshold == 0:
        print("No pre pruning")
    else:
        print("Pre pruning with threshold set at " + str(pre_prune_threshold))
    tree = create_decision_tree(training_instances,trace=0,prune=pre_prune_threshold,class_index=0)
    tree_copy = copy.deepcopy(tree)
    attribute_name_file_path = folder_path + "car_att_names.txt"
    final_tree_tgf_file_path = folder_path + "tree_part2.tgf"
    format_a_tree_to_a_tgf_file(tree,attribute_name_file_path,final_tree_tgf_file_path)
    #print("testing data:")
    #print(testing_instances)
    print("accuracy on training data:: " + str(classification_accuracy(tree_copy,training_instances,0)))
    print("accuracy on testing data:: " + str(classification_accuracy(tree_copy,testing_instances,0)))
    print("recall on training data: " + str(classification_recall(tree_copy,training_instances,0)))
    print("recall on testing data: " + str(classification_recall(tree_copy,testing_instances,0)))
    print()
    print("The following is the original tree output")
    print(treeInfo)
    # end for part2


