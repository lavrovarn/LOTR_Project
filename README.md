# The Lord of the Rings - Relationships between Characters
## Introduction
In this project, I delve into the intricate network of relationships between characters in J.R.R. Tolkien's epic fantasy trilogy, "The Lord of the Rings." Utilizing various data analysis techniques and Python libraries, I aim to uncover the dynamics and significance of these relationships throughout the series.

_This project was developed using Jupyter Notebook_


## Acknowledgements
I would like to express my gratitude to [Thu Vu Data Analytics](https://www.youtube.com/@Thuvu5) for her insightful videos on analyzing character relationships in the Witcher universe. Their work served as inspiration and provided valuable insights that guided the approach taken in this project.

## Project Overview
The project comprises several key steps:

1. Data Collection: Scraping character data from "The Lord of the Rings" movies and books from reputable sources. 
..* [The Lord of the Rings: The Fellowship of the Ring ](https://lotr.fandom.com/wiki/The_Lord_of_the_Rings:_The_Fellowship_of_the_Ring)
..* [The Lord of the Rings: The Two Towers](https://lotr.fandom.com/wiki/The_Lord_of_the_Rings:_The_Two_Towers)
..* [The Lord of the Rings: The Return of the King](https://lotr.fandom.com/wiki/The_Lord_of_the_Rings:_The_Return_of_the_King)
..* [Category:Characters in The Lord of the Rings
](https://tolkiengateway.net/wiki/Category:Characters_in_The_Lord_of_the_Rings)

Because many characters have multiple names, for example Aragorn is also known as Strider and Elessar, I also stored the other names from the personal page of each character. Some characters don't appear in the movies, so I compared the characters from the films with a list of characters from tolkiengateway.net to ensure that all unique characters were included in the dataset.
2. Relationship Extraction: Analyzing the text of the trilogy to extract relationships between characters based on their co-occurrence and interactions.
3. Network Visualization: Constructing a graphical representation of the character network using NetworkX, allowing for intuitive visualization of character connections.
4. Community Detection: Employing community detection algorithms to identify cohesive groups of characters within the network.
5. Character Importance Analysis: Assessing the importance and evolution of characters throughout the series based on metrics such as degree centrality.
6. Word Cloud Generation: Creating word clouds to visually represent the most prominent themes and topics in each book.

## Methodology
I scraped character data from multiple sources, ensuring comprehensive coverage of characters across movies and books. Using Spacy's Named Entity Recognition (NER), I identified character mentions in the text and established relationships based on their frequency of co-occurrence. The constructed network graph visualized character connections, while community detection algorithms revealed groups of characters with strong internal ties. Analyzing character importance over time provided insights into their roles and contributions to the narrative, while word clouds highlighted recurring themes and concepts in each book.

## Used Technologies
..* **Selenium**: Utilized for web scraping character data from online sources such as lotr.fandom.com and tolkiengateway.net.
..* **Spacy**: Employed for Named Entity Recognition (NER) to extract character mentions from the text of the books.
..* **NetworkX**: Used for constructing and visualizing the character network graph, allowing for intuitive exploration of character connections and relationships.
..* **Community Detection Algorithms (Community Louvain)**: Applied to identify cohesive groups of characters within the network, shedding light on distinct communities and their interactions.
..* **WordCloud**: Utilized for generating visual representations of the most prominent themes and topics in each book based on textual analysis.
..* **Matplotlib** and **Pyvis Network**: Employed for visualizing graphs and networks, providing interactive and static representations of character relationships and communities.

## Results 
### Graph
To make the graph more readable, I decided to limit the number of nodes by only including the first 150 rows of the dataset. The dataset was also filtered by the value of the relationships in descending order, so that only the most significant relationships were included in the graph.

Here is the result: 
![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1") 

The visualizations generated using pandas can be challenging to interpret, particularly when attempting to identify dependencies between characters. Therefore, to address this limitation and create more intuitive network visualizations, I opted to utilize Pyvis Network, a powerful tool specifically designed for network analysis and visualization.

### Network 

Here is the link to dynamic graphs visualisation: [Network](https://tolkiengateway.net/wiki/Category:Characters_in_The_Lord_of_the_Rings)

### Insights Based on Characters Network Degree

Based on the degree centrality values, we can draw several insights about the characters' importance within the network:

![alt text](https://github.com/adam-p/markdown-here/raw/master/src/common/images/icon48.png "Logo Title Text 1") 

1. **Frodo Baggins** and **Gandalf** have the highest degree centrality, indicating that they are the most central characters in terms of relationships with other characters. This suggests that they play significant roles and have strong connections with various characters throughout the story.

2. **Samwise Gamgee** follows closely behind Frodo and Gandalf in terms of degree centrality, indicating his crucial role and extensive interactions with other characters, particularly Frodo.

3. **Meriadoc Brandybuck** and **Peregrin Took**, often referred to as Merry and Pippin, also have relatively high degree centrality values, indicating their importance and active involvement in the events of the story, especially within the Fellowship of the Ring.

4. **Aragorn II Elessar**, **Gimli**, **Legolas**, and **Saruman** have moderate degree centrality values, suggesting their significant roles and interactions with other characters, albeit to a lesser extent compared to Frodo, Gandalf, and Samwise.

5. Characters like **Shadowfax**, **Goldberry**, **Tom Bombadil**, **Gorbag**, **Glóin**, **Galadriel**, **Shelob**, **Gildor**, and **Grishnákh** have relatively low degree centrality values, indicating that they have fewer connections with other characters in the network and may have more peripheral roles in the story.

6. Some characters have very low degree centrality values, such as **Rosie Cotton**, **Ted Sandyman**, **Radagast**, **Lotho Sackville-Baggins**, **Imrahil**, **Nazgûl**, **Glorfindel**, **Arathorn**, **Éomund**, **Damrod**, **Mablung (ranger of Ithilien)**, **Warden of the Houses of Healing**, **Thengel**, **Elladan**, **Elrohir**, and **Barliman Butterbur**. These characters likely have minor roles and limited interactions with other characters in the network.


### Communities
I used communities to identify groups of characters within the network who share common characteristics or have similar roles or relationships in the story.  I used the community_louvain package to identify the communities within the LOTR character network. 

Here is the link to dynamic graphs visualisation: [Communities Network](https://tolkiengateway.net/wiki/Category:Characters_in_The_Lord_of_the_Rings)

The character network analysis revealed six distinct communities, each comprising characters with close affiliations and interactions. Based on the communities extracted from the characters network, here are some insights for each community:

**Community 0:**
- This community includes characters like Frodo Baggins, Galadriel, and Sauron.
- It seems to comprise characters associated with mystical or magical elements, such as powerful beings like Sauron and mystical entities like Goldberry and Tom Bombadil.
- The presence of characters like Barliman Butterbur and Lotho Sackville-Baggins suggests a connection to the more mundane aspects of Middle-earth, possibly representing a balance between the ordinary and the extraordinary.

**Community 1:**
- This community includes characters like Bilbo Baggins, Gandalf, and Samwise Gamgee.
- It seems to comprise characters closely associated with the events of the War of the Ring and the Fellowship of the Ring.
- Characters like Gollum and Shelob, who play significant roles in the quest to destroy the One Ring, are also included, highlighting the theme of temptation and corruption.

**Community 2:**
- This community consists of only two characters, Damrod and Mablung.
- These characters are both rangers of Ithilien, suggesting a thematic connection related to their shared duties and responsibilities in guarding Gondor's borders.

**Community 3:**
- This community includes characters like Boromir, Faramir, and Peregrin Took.
- It seems to comprise characters associated with the realm of Gondor and its affairs.
- The presence of characters like Beregond and the Warden of the Houses of Healing suggests a focus on the military and healing aspects of Gondor's society.

**Community 4:**
- This community consists of only two characters, Elladan and Elrohir.
- These characters are twin sons of Elrond, suggesting a thematic connection related to their familial ties and possibly their roles as scouts and warriors.

**Community 5:**
- This community includes characters like Aragorn II, Gimli, and Legolas.
- It seems to comprise characters associated with the events of the War of the Ring, particularly those involved in the quest to destroy the One Ring and the battles against Sauron's forces.
- The presence of characters like Saruman and Gríma Wormtongue suggests a connection to the political and strategic aspects of the war effort.

### Characters' importance over time 

It seems that Frodo and Sam have similar patterns in terms of their degree centrality throughout the books, while Aragorn and Gandalf also have a similar pattern.

**Frodo and Sam** have the highest degree centrality in the first, second, and fourth books because they are the central protagonists of "The Lord of the Rings" trilogy. Their journey to destroy the One Ring forms the core narrative of the story, leading to their frequent interactions with a wide range of characters throughout the books. As a result, they are mentioned more frequently and have more connections to other characters, leading to their higher degree centrality in those particular books.

**Aragorn and Gandalf's** higher degree centrality in the third book may be due to their roles in leading the armies of Men against Sauron's forces in the War of the Ring. They are also involved in important plot points such as the Battle of the Hornburg and the Ride of the Rohirrim, which may have contributed to their increased relationships with other characters. On the other hand, Frodo and Sam are mainly focused on their mission to destroy the One Ring and are separated from the other main characters for much of the book. This may have limited their opportunities for developing relationships and thus their degree centrality.
