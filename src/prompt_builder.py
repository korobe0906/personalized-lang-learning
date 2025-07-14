def build_prompt(topic, keywords, template_path):
    with open(template_path, 'r', encoding='utf-8') as f:
        template = f.read()
    return template.replace("{{topic}}", topic).replace("{{keywords}}", ", ".join(keywords))