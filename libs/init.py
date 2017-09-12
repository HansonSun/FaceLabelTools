from collections import OrderedDict


glb_view_mode=0
save_change=0
glb_label_file=""
glb_input_rule_list=[]
glb_output_rule_list=[]



def from_dict_to_rule(text):
	text=text.strip()
	text=text.split(" ")


	point_cnt=0
	rect_cnt=0

	output_dict=OrderedDict()
	num_index=0
	rule_index=0
	output_dict["flag"]=1
	while num_index<len(text):

		if(glb_output_rule_list[rule_index]=='point'):
			point_cnt+=1
			output_dict["point_%d"%point_cnt]=(int(text[num_index]),int(text[num_index+1]) )
			num_index+=2
			rule_index+=1
		else:
			rect_cnt+=1
			output_dict["rect2p_%d"%rect_cnt]=( (int(text[0]),int(text[1])) ,(int(text[2]),int(text[3]) ) )
			num_index+=4
			rule_index+=1


	return output_dict
