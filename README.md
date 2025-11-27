# Redbus-Web-Scraping-using-Selenium-Streamlit
End-to-end Redbus data pipeline: scrape → store → visualize using Selenium, SQL, and Streamlit.
This project focuses on scraping real-time bus data from Redbus using Selenium Web Automation, processing and storing the extracted information, and visualizing it through an interactive Streamlit dashboard. The system extracts important details such as routes, bus names, timings, prices, ratings, and seat availability, allowing users to easily analyze and filter the information.

The scraping module uses Selenium to navigate Redbus dynamically, handle scrolling and waits, and collect data efficiently from multiple route pages. All scraped data is stored in CSV files and a SQL database, making it easy to access, update, and query.

Once the data is collected, the Streamlit application provides a user-friendly interface to explore the data. Users can filter buses by route, bus type, star rating, price range, or seat availability. Visualizations like bar charts and plots show trends in pricing, ratings, and availability, making the dashboard valuable for analysis and insights.

This project demonstrates end-to-end data engineering skills, including web scraping, database management, data cleaning, and interactive dashboard development,
