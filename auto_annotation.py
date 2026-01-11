import argparse
import threading
import cv2
import json
import os

import metas_create

level = ['defective', 'flawed', 'mediocre', 'standard', 'good', 'fine', 'excellent', 'superior', 'exceptional', 'exemplary']
score = [0,0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0]
perfect_description = "The picture is clear and complete. "

def parse_args():
    parser = argparse.ArgumentParser(description="Auto annotation script.")
    parser.add_argument(
        "--dataset_path",
        type=str,
        required=True,
        help="Input text to be annotated."
    )
    parser.add_argument(
        "--start",
        type=int,
        default=1,
        help="Start index for annotation. Must be >= 1.",
        choices=range(1, 647)
    )
    return parser.parse_args()

def score_to_level(s: float) -> str:
    for i in range(len(score)-1):
        if score[i] <= s < score[i+1]:
            return level[i]
    if s >= 0.99:
        return level[-1]

def description_replace(type_val: str, 
                        texture_level: str, 
                        color_level: str, 
                        structure_level: str, 
                        position: str,
                        types: str,
                        texture_score: float, 
                        color_score: float, 
                        structure_score: float,
                        default_description: str) -> str:
    replacements = {
        "[TYPE]": type_val,
        "[TEXTURE_INFO]": texture_level,
        "[COLOR_INFO]": color_level,
        "[STRUCTURE_INFO]": structure_level,
        "[POSITION]": position,
        "[TYPES]": types,
        "[TEXTURE_SCORE]": str(texture_score),
        "[COLOR_SCORE]": str(color_score),
        "[STRUCTURE_SCORE]": str(structure_score)
    }

    for placeholder, value in replacements.items():
        default_description = default_description.replace(placeholder, value)

    return default_description

def annotate_task(img_name: str, json_data, index):
    default_description = ""
    current_item = json_data[index]

    # 按照种类分，如果是红外，则不需要颜色评分
    if "Infrared" in img_name:
        texture_score = float(input(f"Enter texture score for {img_name} (0.0 - 1.0): "))
        structure_score = float(input(f"Enter structure score for {img_name} (0.0 - 1.0): "))
        texture_level = score_to_level(texture_score)
        structure_level = score_to_level(structure_score)
        # 特判:
        # 分数过高，则替换 "Especially in the [POSITION] area, the [TYPES] imaging is not ideal. " 为Perfect Description
        for i in range(len(metas_create.default_description_list)):
            if i == 1 or i == 6:
                continue
            if i == 3 and texture_level is level[-1] and structure_level is level[-1]:
                default_description += perfect_description
                continue
            default_description += metas_create.default_description_list[i]
        current_item["description"] = description_replace(
                type_val="infrared",
                texture_level=texture_level,
                color_level="",
                structure_level=structure_level,
                position=input(f"Enter '... [POSITION] area': "),
                types=input(f"Enter 'the [TYPES] imaging': "),
                texture_score=texture_score,
                color_score=0.0,
                structure_score=structure_score,
                default_description=default_description
            )
    else:
        texture_score = float(input(f"Enter texture score for {img_name} (0.0 - 1.0): "))
        color_score = float(input(f"Enter color score for {img_name} (0.0 - 1.0): "))
        structure_score = float(input(f"Enter structure score for {img_name} (0.0 - 1.0): "))
        texture_level = score_to_level(texture_score)
        color_level = score_to_level(color_score)
        structure_level = score_to_level(structure_score)
        # 特判:
        # 分数过高，则替换 "Especially in the [POSITION] area, the [TYPES] imaging is not ideal. " 为Perfect Description
        for i in range(len(metas_create.default_description_list)):
            if i == 3 and texture_level is level[-1] and color_level is level[-1] and structure_level is level[-1]:
                default_description += perfect_description
                continue
            default_description += metas_create.default_description_list[i]
        current_item["description"] = description_replace(
                type_val="RGB",
                texture_level=texture_level,
                color_level=color_level,
                structure_level=structure_level,
                position=input(f"Enter '... [POSITION] area': "),
                types=input(f"Enter '... the [TYPES] imaging': "),
                texture_score=texture_score,
                color_score=color_score,
                structure_score=structure_score,
                default_description=default_description
            )

def show_and_annotate(start: int, files_path: str):
    if not os.path.exists(os.path.join(files_path, "Metas.json")):
        metas_create.create_metas_jsons(files_path)
    
    with open(os.path.join(files_path, "Metas.json"), 'r', encoding='utf-8') as f:
        json_data = json.load(f)
    
    print(f"Starting from index {start}, displaying images for annotation...")

    for i in range(start - 1, len(json_data)):
        img_path = os.path.join(files_path, json_data[i]["image_path"])
        img = cv2.imread(img_path)
        img_name = os.path.basename(img_path)

        cv2.imshow(img_name, img)

        t = threading.Thread(target=annotate_task, args=(img_name, json_data, i))
        t.daemon = True
        t.start()

        while t.is_alive():
            cv2.waitKey(100)
        
        with open(os.path.join(files_path, "Metas.json"), 'w', encoding='utf-8') as f:
            json.dump(json_data, f, indent=4, ensure_ascii=False)
        
        print("---------------------------------------------------------------------")

    print(f"Annotation completed for all images of {files_path}.")
    cv2.destroyAllWindows()

if __name__ == "__main__":
    args = parse_args()
    show_and_annotate(args.start, args.dataset_path)