from src.aim_parser import load_ontology, parse_aim
from src.prompt_builder import build_prompt
from src.gpt_client import get_response

ontology = load_ontology("data/ontology_keywords.json")
aim = input("Nhập mục tiêu học (AIM): ")

topics = parse_aim(aim, ontology)
print(" Chủ đề liên quan:", topics)


prompt = build_prompt(topics[0], ontology[topics[0]], "prompts/prompt_template.txt")
print(" Prompt gửi GPT:")
print(prompt)

response = get_response(prompt)
print("\n Kết quả GPT:")
print(response)