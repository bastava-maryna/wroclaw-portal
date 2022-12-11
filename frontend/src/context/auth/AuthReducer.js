/* eslint-disable prettier/prettier */
const authReducer = (state, action) => {
  switch (action.type) {
    case 'SET_IS_AUTHENTICATED':
      return {
        ...state,
        isAuthenticated: action.payload,
        isLoading: false,
      };
    case 'REQUEST_LOGIN':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'LOGIN_SUCCESS':
      return {
        ...state,
        user: action.payload.user,
        token: action.payload.access_token,
        isAuthenticated: true,
        isLoading: false,
        error: null,
      };
    case 'LOGOUT':
      return {
        ...state,
        user: null,
        isLoading: false,
        isAuthenticated: false,
        token: null,
        error: null,
        isEditing: false,
        editError: null,
        editSuccess: false,
        registerError: false,
        modalType: null,
        modalProps: {},
        newThreadLoading: false,
        newThreadSuccess: false,
        newThreadName: '',
        newThreadContent: '',
        newThreadId: null,
        newThreadError: null,
        newThreadShow: false,
      };
    case 'SET_LOADING':
      return {
        ...state,
        isLoading: true,
      };
    case 'RESET':
      return {
        ...state,
        isLoading: false,
        newThreadSuccess: false,
        newPostLoading: false,
      };
    case 'LOGIN_ERROR':
      return {
        ...state,
        error: action.error,
        isLoading: false,
      };
    case 'LOGIN_RESET':
      return {
        ...state,
        isLoading: false,
        isAuthenticated: false,
        user: null,
        token: null,
        error: null,
      };
    case 'REGISTER_REQUEST':
      return {
        ...state,
        isLoading: true,
        registerError: null,
      };
    case 'REGISTER_SUCCESS':
      return {
        ...state,
        isLoading: false,
        registerError: null,
      };
    case 'REGISTER_ERROR':
      return {
        ...state,
        isLoading: false,
        registerError: action.error,
      };
    case 'REGISTER_RESET':
      return {
        ...state,
        isLoading: false,
        registerError: null,
      };
    case 'REQUEST_EDIT_PROFILE':
      return {
        ...state,
        isEditing: true,
        editError: null,
        editSuccess: false,
      };
    case 'EDIT_PROFILE_SUCCESS':
      return {
        ...state,
        isEditing: false,
        editError: null,
        editSuccess: true,
        user: action.payload.user,
      };
    case 'EDIT_PROFILE_FAILURE':
      return {
        ...state,
        isEditing: false,
        editSuccess: false,
        editError: action.error,
      };
    case 'EDIT_PROFILE_RESET':
      return {
        ...state,
        isEditing: false,
        editError: null,
        editSuccess: false,
      };
    case 'SHOW_MODAL':
      return {
        ...state,
        modalType: action.modalType,
        modalProps: action.modalProps,
      };
    case 'HIDE_MODAL':
      return {
        ...state,
        modalType: null,
        modalProps: {},
      };
    case 'CREATE_THREAD_TOGGLE':
      return {
        ...state,
        newThreadShow: !state.newThreadShow,
        newThreadSuccess: false,
        newThreadError: null,
      };
    case 'CREATE_THREAD_REQUEST':
      return {
        ...state,
        newThreadLoading: true,
        newThreadSuccess: false,
        newThreadError: null,
        newThreadName: action.newThread.thread_name,
        newThreadContent: action.newThread.thread_content,
      };
    case 'CREATE_THREAD_SUCCESS':
      return {
        ...state,
        newThreadLoading: false,
        newThreadSuccess: true,
        newThreadName: '',
        newThreadContent: '',
        newThreadId: action.newThread.thread['thread_id'],
        newThreadShow: false,
        newThreadError: null,
      };
    case 'CREATE_THREAD_FAILURE':
      return {
        ...state,
        newThreadLoading: false,
        newThreadSuccess: false,
        newThreadId: null,
        newThreadShow: true,
        newThreadError: action.error,
      };
    case 'CREATE_THREAD_SAVE':
      return {
        ...state,
        newThreadName: action.threda_name,
        newThreadContent: action.thread_content,
      };
    case 'DELETE_THREAD_REQUEST':
      return {
        ...state,
        isDeleting: true,
        deleteError: null,
      };
    case 'DELETE_THREAD_SUCCESS':
      return {
        ...state,
        isDeleting: false,
        deleteError: null,
        //newThreadId: null,
        name: null,
      };
    case 'DELETE_THREAD_FAILURE':
      return {
        ...state,
        isDeleting: false,
        deleteError: action.error,
      };
    case 'FETCH_TOPIC_REQUEST':
      return {
        ...state,
        newThreadLoading: false,
        newThreadSuccess: false,
        newThreadId: null,
        newThreadError: null,
        newThreadShow: false,
        isLoading: true,
        error: null,
      };
    case 'FETCH_TOPIC_SUCCESS':
      return {
        ...state,
        isLoading: false,
        name: action.name,
        //slug: action.slug,
        //description: action.description,
        threads: action.threads,
        error: null,
      };
    case 'FETCH_TOPIC_FAILURE':
      return {
        ...state,
        error: action.error,
      };
    //---posts
    case 'CREATE_POST_REQUEST':
      return {
        ...state,
        newPostLoading: true,
        newPostError: null,
        newPostSuccess: false,
      };
    case 'CREATE_POST_SUCCESS':
      return {
        ...state,
        newPostLoading: false,
        newPostError: null,
        newPostSuccess: true,
      };
    case 'CREATE_POST_FAILURE':
      return {
        ...state,
        newPostLoading: false,
        newPostError: action.error,
        newPostSuccess: false,
      };
    case 'DELETE_POST_REQUEST':
      return {
        ...state,
        deletePostList: [...state.deletePostList, action.id],
      };
    case 'DELETE_POST_SUCCESS':
    case 'DELETE_POST_FAILURE':
      return {
        ...state,
        deletePostList: state.deletePostList.filter((id) => id !== action.id),
      };
    case 'FETCH_THREAD_REQUEST':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'FETCH_THREAD_SUCCESS':
      return {
        ...state,
        isLoading: false,
        curThread: action.thread,
        //curThread: action.payload,
        name: action.thread ? action.thread.thread_name : null,
        //thread_name: action.payload.thread_name,
        //name: action.thread.name,
        //content: action.thread.content,
        //pinned: action.thread.pinned,
        //creator: action.thread.creator,
        //createdAt: action.thread.created_at,
        //posts: action.thread,
        error: null,
      };
    case 'FETCH_THREAD__POST_SUCCESS':
      return {
        ...state,
        posts: action.posts,
      };
    case 'FETCH_THREAD_FAILURE':
      console.log('error in delete thread reducer');
      console.log(action);
      return {
        ...state,
        isLoading: false,
        error: action.error,
      };
    default:
      return state;
    //throw new Error(`Unhandled action type: ${action.type}`);
  }
};

export default authReducer;
