from collections import OrderedDict


glb_view_mode=0
glb_save_change=0
glb_labelfile_path=""
glb_imgfile_path=""
glb_input_rule_list=[]
glb_output_rule_list=[]
glb_7p_warning=True
glb_auto_put_7p=True


def from_dict_to_rule(text):
	text=text.strip()
	text=text.split(" ")

	point_cnt=0
	rect_cnt=0
	output_dict=OrderedDict()

	if( len(text)!=14):
		return output_dict
	else:

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
				output_dict["rect2p_%d"%rect_cnt]=( (int(text[num_index]),int(text[num_index+1])) ,(int(text[num_index+2]),int(text[num_index+3]) ) )
				num_index+=4
				rule_index+=1


		return output_dict
