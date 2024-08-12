This project consists of two main directories.
Each directory displays a different user interface on the web browser.
The goal is to compare and contrast the responses of these systems.
Please do not delete any files in this project such as user_stomach , next_meal.json etc, as they will store temporary data needed to successfully run the project.

The main directories are kg_llm and vector_embedded_llm. 
To run this project, you require an OpenAI subscription or free account that provides you with an OpenAI key, which you will place in your .env file in both the kg_llm and vector_embedded_llm directories.
Your .env file should look like this: OPENAI_API_KEY=put_your_key_here
You also need a Neo4J free or paid subscription that provides you with a Neo4J account, database instance, password and Neo4J connection URL.

To create your knowledge graph, open the kg_llm folder, and in that folder, open the data folder. 
Run the graph_maker.py script with your Neo4J credentials for the connection_URL and password, make sure all the files such as compound_health_effects, foods.json, compounds.json, health_effects.json, recommended_daily_allowance.json are present in that directory.
After the graph is created, which will take some time- maybe over an hour, since there are 60,000 compounds, confirm it's content by accessing your Neo4j dashboard on the web.

Step II:Running the LLM, with data from the graph

Now go the kg_llm directory and run the main.py file, use pip to install all necessary packages.
Fill in your OpenAI and Neo4j Credentials as needed in the script.
Run the python file, a message should appear in the console telling you how to run the streamlit app by pasting your path in the terminal, i.e streamlit run your-path-to-main.py
You should see the streamlet app running in your browser now, and you may proceed interact with the User interface.

Step III: Running the LLM with data from a vector database
Now go to the vector_embedded_llm directory and open the VectorDB.py file; all the pdf files you need for embedding will be found in the data folder in the vector_embedded_llm directory.

Run the VectorDB python file, a message should appear in the console telling you how to run the streamlit app, by pasting your path in the terminal i.e streamlit run your-path-to-VectorDB.py 
You should see the streamlit app running in your browser now, and you may proceed to interact with the User interface.

Step IV: 
Using the user interface of the applications is intuitive. In the case of System B, select from drop-down menus and use sliders to select the number of meals eaten or desired. In the case of System A, ask the chatbot a question to evaluate your meal choices.
