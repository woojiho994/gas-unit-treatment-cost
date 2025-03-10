import pandas as pd
from openai import OpenAI

class CostEstimator:
    def __init__(self, excel_path):
        """初始化成本估算器"""
        self.df = pd.read_excel(excel_path)
        self.client = OpenAI(
            api_key="sk-mpICptPNOSJt3uTlllxSJXIS00aOVGRKSgnHsEgGyUjpcrlC",  # 在这里直接填入你的API密钥
            base_url="https://api.moonshot.cn/v1"
        )

    def get_cost_estimation(self, industry_type, pollutant_type):
        """获取治理成本估算"""
        # 只按污染物类型筛选数据
        filtered_data = self.df[
            self.df['污染物类型'].str.contains(pollutant_type, na=False)
        ]

        # 准备提示信息
        context = f"基于以下数据:\n{filtered_data.to_string()}\n"
        prompt = f"{context}\n请分析{industry_type}行业处理{pollutant_type}的单位治理成本。给出合理的成本估算范围和建议。"

        # 调用Moonshot AI API
        response = self.client.chat.completions.create(
            model="moonshot-v1-8k",
            messages=[
                {"role": "system", "content": "你是一个环保治理成本分析专家，请基于历史数据提供专业的成本估算建议，并给出合理的成本建议,回答尽可能简单。"},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1
        )

        return response.choices[0].message.content

def main():
    # 使用示例
    estimator = CostEstimator('废气处理.xlsx')
    
    while True:
        print("\n=== 污染物治理成本估算系统 ===")
        industry = input("请输入行业类型（输入'q'退出）: ")
        if industry.lower() == 'q':
            break
            
        pollutant = input("请输入污染物类型: ")
        
        try:
            result = estimator.get_cost_estimation(industry, pollutant)
            print("\n分析结果：")
            print(result)
        except Exception as e:
            print(f"发生错误: {e}")

if __name__ == "__main__":
    main() 