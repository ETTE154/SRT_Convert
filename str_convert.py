import re
import openai

class SceneAnalyzer:
    def __init__(self, api_key, filename):
        self.api_key = api_key
        self.filename = filename
        openai.api_key = self.api_key

    def scene_analysis(self, content):
        response = openai.ChatCompletion.create(
            model="gpt-4-0613",
            messages=[
                {"role": "system", "content": "You are a helpful assistant that rates the intensity of described scenes on a scale of 0 (calm) to 10 (intense). Please respond with a whole number between 0 and 10."},
                {"role": "user", "content": f"This is a scene description: '{content}'."},
            ]
        )

        try:
            intensity = round(float(response['choices'][0]['message']['content'].strip()))
            if 0 <= intensity <= 10:
                return intensity
            else:
                raise ValueError()
        except ValueError:
            print(f"Unexpected response: {response['choices'][0]['message']['content'].strip()}")
            print("Retrying with a median intensity...")
            
            # Retry with median intensity
            response = openai.ChatCompletion.create(
                model="gpt-4-0613",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that rates the intensity of described scenes on a scale of 0 (calm) to 10 (intense). Please respond with a whole number between 0 and 10."},
                    {"role": "user", "content": f"This is a scene description: '{content}'. The scene is of medium intensity."},
                ]
            )

            try:
                intensity = round(float(response['choices'][0]['message']['content'].strip()))
                if 0 <= intensity <= 10:
                    return intensity
                else:
                    print(f"Unexpected response on retry: {response['choices'][0]['message']['content'].strip()}")
                    return None
            except ValueError:
                print(f"Unexpected response on retry: {response['choices'][0]['message']['content'].strip()}")
                return None


    def extract_bracket_content_and_time(self):
        with open(self.filename, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            
        bracket_contents_with_time = []
        current_time = None
        
        pattern = re.compile(r'\[(.*?)\]')

        for line in lines:
            line = line.strip()
            if '-->' in line: 
                current_time = line
            else:
                matches = pattern.findall(line)
                if matches:
                    for match in matches:
                        bracket_contents_with_time.append((current_time, match))
                        
        return bracket_contents_with_time

    def process_subtitle(self):
        bracket_contents_with_time = self.extract_bracket_content_and_time()
        
        for i in range(len(bracket_contents_with_time)):
            time, content = bracket_contents_with_time[i]
            intensity = self.scene_analysis(content)
            if intensity is not None:
                bracket_contents_with_time[i] = (time, intensity)

        return bracket_contents_with_time

if __name__ == "__main__":
    analyzer = SceneAnalyzer('api-key', 'srt_dir')
    results = analyzer.process_subtitle()
    print(results)