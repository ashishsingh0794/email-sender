import jinja2


class TemplateLoader:
    def __init__(self, template_folder : str, template_file : str):
        self.template_folder = template_folder
        self.template_file = template_file
        
    def get_template_text(self, **kwargs : dict) -> str:
        templateLoader = jinja2.FileSystemLoader(searchpath=self.template_folder)
        templateEnv = jinja2.Environment(loader=templateLoader)
        template = templateEnv.get_template(self.template_file)
        outputText = template.render(**kwargs)
        
        return outputText