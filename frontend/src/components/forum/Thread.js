import React, { useContext } from 'react';
import { Segment, Icon } from 'semantic-ui-react';
import StatusMessage from './StatusMessage';
import Post from './Post';
import NewPost from './NewPost';
import AuthContext from '../../context/auth/AuthContext';

const Thread = ({
  //isDeleting,
  //deleteError,
  thread,
  posts,
  createPost,
  deletePost,
  deleteThread,
}) => {
  const {
    dispatch,
    isAuthenticated,
    isLoading,
    error,
    user,
    isDeleting,
    deleteError,
    deletePostList,
    name,
  } = useContext(AuthContext);
  const {
    thread_id,
    thread_name,
    thread_content,
    thread_created_at,
    //thread_creator,
    pinned,
    avatar,
    user_name,
    //user_email,
  } = thread;

  if (error || deleteError || isLoading || isDeleting || !name) {
    let loadingMessage = 'We are fetching the thread for you';
    if (isDeleting) {
      loadingMessage = 'We are deleting the thread for you';
    }
    console.log('!name');
    console.log(!name);
    return (
      <StatusMessage
        error={error || deleteError || !name} // because a thread name cannot be empty
        errorClassName="thread-error"
        errorMessage={error || deleteError}
        loading={isLoading || isDeleting}
        loadingMessage={loadingMessage}
        nothing={!name}
        nothingMessage={'Thread does not exist'}
        type="default"
      />
    );
  }

  const threadPost = (
    <Post
      id={thread_id}
      threadID={thread_id}
      isThread={true}
      content={thread_content}
      createdAt={thread_created_at}
      creator={user_name}
      creator_name={user_name}
      avatar={avatar}
      deleteAction={deleteThread}
      dispatch={dispatch}
      authenticatedUserName={user?.user_name}
    />
  );

  return (
    <div className="threadContainer">
      <div className="thread-title">
        <Icon name={pinned ? 'pin' : 'comment alternate outline'} />
        {thread_name}
      </div>
      <Segment.Group className="thread-list">
        {threadPost}
        {posts &&
          posts.map((post) => (
            <Post
              key={post.post_id}
              //post={post}
              threadID={thread_id}
              id={post.post_id}
              isThread={false}
              content={post.post_content}
              createdAt={post.post_created_at}
              creator={post.post_creator}
              creator_name={post.post_creator_name}
              authenticatedUser={user}
              authenticatedUserName={user?.user_name}
              avatar={post.avatar}
              deletePostList={deletePostList}
              deleteAction={deletePost}
              dispatch={dispatch}
            />
          ))}
      </Segment.Group>
      <NewPost
        isAuthenticated={isAuthenticated}
        threadID={thread_id}
        authenticatedUser={user}
        authenticatedUserName={user?.user_name}
        createPost={createPost}
        //success={newPostSuccess}
        //isLoading={newPostLoading}
        //error={newPostError}
        maxLength={2000}
        dispatch={dispatch}
      />
    </div>
  );
};

export default Thread;
