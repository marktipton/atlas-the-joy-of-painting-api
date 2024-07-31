# The Joy of Painting ETL Project

## Project Context

In this project, we are going to explore the idea of ETL (Extract, Transform, Load), which is the process of taking data from multiple unique sources, modifying them in some way, and then storing them in a centralized database. This is a very common practice when collecting data from systems in order to utilize that data in another system. This data may come in the form of CSV, JSON, XML, API requests with other custom formats, etc. It might even be that you have direct access to several databases with different, but relatable data that you want to merge into another database in order to gain insight from it in some way.

## Presented Problem

Your local public broadcasting station has an overwhelming amount of requests for information on *The Joy of Painting*. Their viewers want a website that allows them to filter the 403 episodes based on the following criteria:

- **Month of original broadcast**
  - Useful for viewers who wish to watch paintings that were done during the same month of the year.

- **Subject Matter**
  - Useful for viewers who wish to watch specific items get painted.

- **Color Palette**
  - Useful for viewers who wish to watch specific colors being used in a painting.

## Tasks

1. **Extract Data:**
   - Gather data from multiple unique sources (e.g., CSV, JSON, XML, API requests).
   - Ensure that all relevant data about the episodes of *The Joy of Painting* is collected.

2. **Transform Data:**
   - Clean and normalize the collected data.
   - Transform the data into a consistent format that can be easily loaded into the database.
   - Ensure data integrity and handle any discrepancies in the collected data.

3. **Load Data:**
   - Design a centralized database schema that accommodates all necessary fields and relationships.
   - Load the transformed data into the database.
   - Ensure efficient indexing and querying capabilities.

4. **Build API:**
   - Develop an API that allows access to the centralized database.
   - Implement endpoints to filter episodes based on the following criteria:
     - Month of original broadcast.
     - Subject Matter.
     - Color Palette.

## Commands and queries:

  - Get information about all episodes:
    - http://localhost:3000/episodes/

  - Get information about all of the colors used by Bob Ross:
    - http://localhost:3000/episodes/colors

  - Get a list of subjects present in bob ross paintings:
    - http://localhost:3000/episodes/subjects

  - Find all episodes from February:
    - http://localhost:3000/episodes/month?month=2

  - Get episodes where Bob used Phthalo Blue and Dark Sienna:
    - http://localhost:3000/episodes/colors?colors=Dark_Sienna, Phthalo_Blue

  - Get episodes that contain a boat and a dock
    - http://localhost:3000/episodes/subjects?subjects=BOAT,DOCK

