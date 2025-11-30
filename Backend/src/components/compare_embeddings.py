from src.utils.header import  torch,  setup_logger 
logger =setup_logger()

''' we are using similarity score using cosineSimilarity to calucalate how much similar are emebedding of image  are 
with stored emebedding here we have 2 stages to confirm 
    1) if similarity socre is greater than 0.8 we are direclty confirm it is the  best emebeddings 
    2 ) if the similarity score is less than 0.8 /threshold level then we are using another alogritm which 
    combination of low_threshold lvel + majority voter 

'''


# --------------compare embeddings-------------------------------------

def compare_with_embeddings(features_tensor, class_embeddings, device):
    similarity_threshold = 0.8 
    similarity = torch.nn.CosineSimilarity(dim=1)
    features_tensor = features_tensor / features_tensor.norm(dim=1, keepdim=True)
    scores=[]
    for usn, list_of_embedding_lists in class_embeddings.items():
        for db_embedding_list_name , db_embedding_list in list_of_embedding_lists.items():
            try:
                embedding_tensor = torch.tensor(db_embedding_list, dtype=torch.float32).to(device)
                if embedding_tensor.dim() == 1:
                    embedding_tensor = embedding_tensor.unsqueeze(0)
                
                if embedding_tensor.shape[1] != features_tensor.shape[1]:
                    logger.warning(f"Embedding shape mismatch for USN {usn}. DB: {embedding_tensor.shape}, Frame: {features_tensor.shape}. Skipping.")
                    continue
                
                embedding_tensor = embedding_tensor / embedding_tensor.norm(dim=1, keepdim=True)
                
                sim_score = similarity(features_tensor, embedding_tensor).item()
               
                logger.debug(f"Comparing with USN {usn}: similarity = {sim_score:.4f}")
                logger.info(f"Comparing with USN {usn} embedding {db_embedding_list_name}: similarity = {sim_score:.4f}")
                scores.append((usn, sim_score))
                
                    
            except Exception as e:
                logger.error(f"Error comparing embedding for USN {usn}: {e}. Embedding data (type {type(db_embedding_list)}): {str(db_embedding_list)[:50]}...")
    
    scores=sorted(scores, key=lambda x: x[1], reverse=True)[:7]
   
    if scores and scores[0][1] >= similarity_threshold:
        logger.debug(f"Match found: USN {scores[0][0]} with score {scores[0][1]:.4f}")
        return scores[0]  # Return the USN and score of the best match
    else:

        usn_count={}
        for usn, score in scores:
            if usn not in usn_count:
                usn_count[usn]=[0 ,0]
            usn_count[usn]=[usn_count[usn][0]+1 , usn_count[usn][1]+score]
            if usn_count[usn][0]>=3 and (usn_count[usn][1]/usn_count[usn][0])>=0.5: 
                logger.debug(f"Match found by majority voting: USN {usn} with score {score:.4f}")
                return usn, score
           
           
    
    logger.debug("No match found above threshold for this face")
    return None
