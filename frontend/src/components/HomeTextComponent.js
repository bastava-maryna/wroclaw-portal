/* eslint-disable prettier/prettier */

import React from 'react';
import ListGroup from 'react-bootstrap/ListGroup';

import Card from 'react-bootstrap/Card';
import { CardImg } from 'react-bootstrap';
import '../css/App.css';
function HomeTextComponent() {
  return (
    
  <center>
    <Card border="light" style={{ width: '50rem' }}>
      <Card.Body>
        <h1>Wroc(love)</h1>
        <h2 className="mb-2 text-muted">The city to fall in love with</h2>
        <Card.Img variant="top" width="300px" height="300px" src="https://ocdn.eu/pulscms-transforms/1/XDvk9kpTURBXy9hZmZmNGU1ODBjZmI5NGI4YTRmZWZlNjIxMTNjMzgzYy5qcGeTlQPNAe4AzRvHzQ-gkwXNBLDNAqSTCaY2MjI0MDAG3gABoTAB/wroclaw.jpg"/>
        <Card.Text>
          The capital of Lower Silesia (Dolny Slask) has a huge Old Town built on several islands connected by over 100 bridges. Apart from its unique location, Wroclaw amazes with its volume of Gothic, Baroque and Art Nouveau architecture. Several musical and theatre festivals, as well as its busy nightlife, attract innumerable visitors from all over Poland and abroad. Wroclaw’s extremely complicated history, combining the cultural influences of Germany, Bohemia, Austria and Poland, has left its mark on the atmosphere of the city.
          Wroclaw is the principal city of Lower Silesia, a voivodship situated in the south-western corner of Poland, adjoining the German and Czech territories. Its population of 632,000 makes it the fourth largest city in Poland.

The Old Town is comparable to Krakow’s in beauty and size, and includes the Gothic St. John’s Cathedral, the Renaissance houses near the Market Square, the Baroque university and lots of fine examples of Art Nouveau and Functionalism.

Apart from these sights, Wroclaw captivates with its marvellous location on the Odra River, its branches and tributaries that have resulted in a great number of bridges needed to join the islands. Despite Wroclaw’s failure to become the host city for the Expo exhibition in 2002, it has undergone a significant boom in terms of tourism. The intense promotion of the city resulted in a rising number of visitors.

The uniqueness of the city is due in part to its long and entangled history. Situated on the interface between ethnically diverse areas, Wroclaw has been part of the Polish, Czech, Austrian and German states. It has inherited the spirit of German Breslau (a previous name of Wroclaw), which partly disappeared when the Germans left the city, and that of Polish Lwow, whose population was resettled here after World War II. Wroclaw is also an important cultural and academic centre of the region, with a large student community that animates the city’s nightlife.
        </Card.Text>
       
      </Card.Body>

       <Card.Body>
        <Card.Title className='title_list'>Your first steps to move to Wrocław:</Card.Title>
        
        <Card.Text>
          <ListGroup variant="flush" className='main_list'>
          <ListGroup.Item action href="/uni"> 1. Find yourself a university</ListGroup.Item>
          <ListGroup.Item action href="/docs"> 2. Learn about your legal stay</ListGroup.Item>
          <ListGroup.Item action href="/map"> 3. Get familiar with the city </ListGroup.Item>
          <ListGroup.Item action href="/forum"> 4. Find out more about life in Wrocław </ListGroup.Item>
          <ListGroup.Item action href="/qa"> 5. Ask your questions </ListGroup.Item>
          <ListGroup.Item action href="/news"> 6. See what is happening in the city </ListGroup.Item>
          <ListGroup.Item > Start your new life! </ListGroup.Item>
    </ListGroup>
        </Card.Text>
        
      </Card.Body>
    </Card>
    </center>
    
  );
}

export default HomeTextComponent;