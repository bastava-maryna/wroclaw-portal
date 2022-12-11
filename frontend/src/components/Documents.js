/* eslint-disable prettier/prettier */
import { useEffect, useState ,useMemo} from 'react';
import ListGroup from 'react-bootstrap/ListGroup';
import Dropdown from 'react-bootstrap/Dropdown';
import {Col,Row} from 'react-bootstrap'
import axios from 'axios';
import '../css/doc_component.css';
import Accordion from 'react-bootstrap/Accordion';

const Documents = () => {
  const [categories,setCategories]=useState([]);
  const [documents,setDocuments]=useState([]);
  const [catID,setCatID]=useState();
  const handleClick=(e)=>{
    setCatID( parseInt(e.target.value));
    console.log(catID);


    
    
  };

  // function getFilteredList() {
  //   if (!setCatID) {
  //     return NaN;
  //   }
        
  //   return documents.filter(doc=>doc.categoryID===catID);
   
  // }
  // var filteredDocs = useMemo(getFilteredList, [catID, documents]);

  

  useEffect(()=>{
    const getData=async()=>{
      const {data}  = await axios.get(
        'http://localhost:5000/docs'
      );
    
      setCategories(data[0]);
      setDocuments(data[1]);
      // console.log(documents[0])
      
    };
    getData();
  },[categories,documents]);
  
  return (
  <div>    
  
    {/* <center>
    <h1 className='doc_title'>Documents </h1>
    </center> */}
    {/* <Row>
      
      <Col lg={3} md={6} sm={10} xs={10} >
      
      <ListGroup variant="flush active"  className='line flex-column align-items-start active mt-5' 
      value={categories} >
         {categories.map((category_arr)=>{
          return (
             <ListGroup.Item  
             action onClick={handleClick}
             
             key={category_arr[0]} 
             value={category_arr[0]} 
             >{category_arr[1]}</ListGroup.Item>
            )
         })}

      </ListGroup>  

      
      </Col> 
      
      <Col >
      <div className='documents' >
      <ListGroup variant="flush active" value={documents}>
         {filteredDocs.map((documents_arr)=>{
           
          return(
            <div >
         
             <ListGroup.Item 
             role="tabpanel"
             key={documents_arr.id}
             id={documents_arr.id}
             action href={documents_arr.link}
             >{documents_arr.name}</ListGroup.Item>
         
          </div>
            )
         }
        )}
      </ListGroup> 
      </div> 
      </Col>  
      </Row> */}


      
     <center>
    <h1 className='doc_title'>Documents </h1>
    </center><br />
      
      {categories.map((category_arr)=>{
          return (
            <Accordion value={categories}>
            <Accordion.Item eventKey="1">
            <Accordion.Header 
             action onClick={handleClick}
             
             key={category_arr[0]} 
             value={category_arr[0]} 
             >{category_arr[1]}</Accordion.Header>
             <Accordion.Body >
             <ListGroup value={documents}>
             {documents.filter(doc=>doc.categoryID===category_arr[0]).map((documents_arr)=>{
           
           return(
             <div >
              
              <ListGroup.Item 
              role="tabpanel"
              key={documents_arr.id}
              id={documents_arr.id}
              action href={documents_arr.link}
              >{documents_arr.name}</ListGroup.Item>
          
           </div>
             )
          }
        )}
        </ListGroup>
        </Accordion.Body>
      </Accordion.Item>
      </Accordion>
            )
         })}
     
        
      
    
      
    
    </div>  
  );
};
export default Documents;
