from report_generator.predict_file import Pipeline, model

# def main(csv_path):

#     try:

#         # print("Reading CSV...")
#         context = predict_delay(csv_path)

#         # print("Creating Chain...")
#         chain = prompt | llm | structure_output

#         # print("Calling LLM...")
#         response = chain.invoke({"context":context})

#         # print("Generate Response...")
#         # if response:
#         #     print(response)
#         # else:
#         #     print("Response is Null.")

#         return response

#     except Exception as e:
#         raise f"Error : {e}"

class PipelineRunner:
    def __init__(self, llm, pipeline, prompt, structure_output):
        self.llm = llm
        self.pipeline = pipeline
        self.prompt = prompt
        self.structure_output = structure_output

    def run(self):
        df = self.pipeline.read_csv()
        X, y = self.pipeline.split_feature(df)
        X = self.pipeline.change_dtype(X)
        quality_report = self.pipeline.check_data_quality(X)
        prediction_report = self.pipeline.prediction_report(X,y)

        context = {
            "Dataset quality report":quality_report,
            "Prediction report":prediction_report
        }

        chain = self.prompt | self.llm | self.structure_output

        response = chain.invoke({"context":context})

        if response:
            return response
        else:
            raise ValueError("No Response Found.")