import json
import os
import argparse

from natsort import natsorted

default_description_list = [
	"This [TYPE] image's texture information is [TEXTURE_INFO], ",
	"color information is [COLOR_INFO], ",
	"and structural information is [STRUCTURE_INFO]. ",
	"Especially in the [POSITION] area, the [TYPES] imaging is not ideal. ",
	"The scores are as follows: ",
	"[TEXTURE_SCORE], ",
	"[COLOR_SCORE], ",
	"[STRUCTURE_SCORE]."
]

def parse_args():
	parser = argparse.ArgumentParser(description="Create Metas.json for image datasets.")
	parser.add_argument(
		"--dataset_path",
		type=str,
		default="./group_01",
		help="Path to the dataset directory containing images."
	)
	return parser.parse_args()

def create_metas_jsons(dir: str, json_file = "Metas.json"):
	target_file = os.path.join(dir, json_file)
	# 如果有JSON，直接return
	if os.path.exists(target_file):
		return

	extensions = ('.png', 'jpg', '.jpeg')
	json_data = []

	if os.path.exists(dir):
		sort_files = natsorted(os.listdir(dir))
		for file in sort_files:
			if file.lower().endswith(extensions):
				default_description = ""
				if "Infrared" in file:
					for i in range(len(default_description_list)):
						# 不需要颜色评分
						if i == 1 or i == 6:
							continue
						default_description += default_description_list[i]
				else:
					default_description = ''.join(default_description_list)
				items = {
					"image_path": file,
					"task_prompt": "Fusion Analysis",
					"description": default_description
				}
				json_data.append(items)
	else:
		print(f"The directory does not exist: {dir}")
		return

	if json_data:
		try:
			with open(target_file, 'w', encoding='utf-8') as f:
				json.dump(json_data, f, ensure_ascii=False, indent=4)
			print(f"Created {target_file} with {len(json_data)} entries.")
		except Exception as e:
			print(f"An error occurred while writing to {target_file}: {e}")
	else:
		print("No image files found to process.")		

# Test
# if __name__ == "__main__":
# 	args = parse_args()
# 	dataset_path = args.dataset_path
# 	if os.path.exists(dataset_path):
# 		create_metas_jsons(dataset_path)
# 	else:
# 		print(f"The specified dataset path does not exist: {dataset_path}")