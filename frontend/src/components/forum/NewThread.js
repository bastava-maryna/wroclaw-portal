import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import { getSelectedBlock } from 'draftjs-utils';
import htmlToDraft from 'html-to-draftjs';
import { List } from 'immutable';
import {
  EditorState,
  ContentState,
  convertFromRaw,
  convertToRaw,
  Modifier,
} from 'draft-js';
import { Form, Icon, Divider } from 'semantic-ui-react';
import { Button } from 'react-bootstrap';
import './style.css';
import RichEditor from './RichEditor';
import StatusMessage from './StatusMessage';

export default class NewThread extends Component {
  constructor(props) {
    super(props);
    const { thread_name, thread_content } = this.props;
    let editorState = this.convertToEditorState(thread_content);
    this.state = {
      thread_name,
      editorState,
    };
  }

  UNSAFE_componentWillReceiveProps(newProps) {
    const { thread_name: newName, thread_content: newContent } = newProps;
    const editorState = this.convertToEditorState(newContent);
    this.setState({
      thread_name: newName,
      editorState,
    });
  }

  convertToEditorState = (thread_content) => {
    let editorState = EditorState.createEmpty();
    if (thread_content) {
      try {
        const contentState = convertFromRaw(JSON.parse(thread_content));
        editorState = EditorState.createWithContent(contentState);
      } catch (error) {
        const contentState = ContentState.createFromText(thread_content);
        editorState = EditorState.createWithContent(contentState);
      }
    }
    return editorState;
  };

  toggleShowEditor = () => {
    this.props.toggleShowEditor();
  };

  onCancel = () => {
    // reset & clear everything
    const editorState = EditorState.createEmpty();
    this.setState({
      thread_name: '',
      editorState,
    });
    const thread_content = JSON.stringify(
      convertToRaw(editorState.getCurrentContent())
    );
    this.props.updateNewThread({
      thread_name: '',
      thread_content: thread_content,
    });
    this.toggleShowEditor();
  };

  onNameChange = (e, { value }) => {
    this.setState({
      thread_name: value,
    });
  };

  onEditorStateChange = (editorState) => {
    this.setState({
      editorState,
    });
  };

  isFormValid = () => {
    const { thread_name } = this.state;
    return thread_name;
  };

  onSubmit = () => {
    const { dispatch, user } = this.props;
    if (this.isFormValid()) {
      const { thread_name, editorState } = this.state;
      const { topic, createThread } = this.props;
      const thread_content = JSON.stringify(
        convertToRaw(editorState.getCurrentContent())
      );
      let newThread = {
        thread_name: thread_name,
        topic: topic,
        thread_content: thread_content,
        thread_creator: user.user_id,
        pinned: false,
      };
      createThread(dispatch, newThread);
    }
  };

  isValidLength = (contentState) => {
    const maxLength = this.props.maxLength || 100;
    return contentState.getPlainText('').length <= maxLength;
  };

  handleBeforeInput = (input) => {
    const { editorState } = this.state;
    if (!this.isValidLength(editorState.getCurrentContent())) {
      return 'handled';
    }
  };

  handlePastedText = (text, html, editorState, onChange) => {
    if (html) {
      const contentBlock = htmlToDraft(html);
      let contentState = editorState.getCurrentContent();
      contentBlock.entityMap.forEach((value, key) => {
        contentState = contentState.mergeEntityData(key, value);
      });
      contentState = Modifier.replaceWithFragment(
        contentState,
        editorState.getSelection(),
        new List(contentBlock.contentBlocks)
      );
      if (!this.isValidLength(contentState)) {
        return 'handled';
      }
      onChange(
        EditorState.push(editorState, contentState, 'insert-characters')
      );
      return true;
    }
    const selectedBlock = getSelectedBlock(editorState);
    const newState = Modifier.replaceText(
      editorState.getCurrentContent(),
      editorState.getSelection(),
      text,
      editorState.getCurrentInlineStyle()
    );
    if (!this.isValidLength(newState)) {
      return 'handled';
    }
    onChange(EditorState.push(editorState, newState, 'insert-characters'));
    if (selectedBlock && selectedBlock.type === 'code') {
      return true;
    }
    return false;
  };

  render() {
    const { isAuthenticated, isLoading, success, id, error, showEditor } =
      this.props;
    const { thread_name, editorState } = this.state;
    if (!isAuthenticated) {
      return <div className="newThread-none" />;
    }

    const statusMessage = (
      <StatusMessage
        error={error}
        errorClassName="newThread-message"
        errorMessage={error || 'Oops! Something went wrong.'}
        success={success}
        successClassName="newThread-message"
        successMessage={
          <Link to={`/forum/threads/${id}`}>
            {'Successful on creating thread'}
          </Link>
        }
        type="modal"
      />
    );

    if (!showEditor) {
      return (
        <div>
          {statusMessage} {/*this will only show the success message*/}
          <div className="newThread-hidden ">
            <Button
              className="mt-3 w-60"
              variant="custom"
              type="submit"
              onClick={this.toggleShowEditor}
            >
              <i className="fa-solid fa-pen-to-square"></i> &nbsp; New Thread
            </Button>
          </div>
        </div>
      );
    }

    return (
      <div className="newThread-show">
        {statusMessage}
        <Form loading={isLoading} className="attached fluid segment">
          <Form.Input
            required
            fluid
            transparent
            icon="edit"
            iconPosition="left"
            size="big"
            placeholder="Name"
            type="text"
            name="name"
            value={thread_name}
            onChange={this.onNameChange}
          />
          <Divider />
          <RichEditor
            placeholder="Start typing your thread content here..."
            editorState={editorState}
            wrapperClassName="newThread-wrapper"
            toolbarClassName="newThread-toolbar"
            editorClassName="newThread-editor"
            onEditorStateChange={this.onEditorStateChange}
            handleBeforeInput={this.handleBeforeInput}
            handlePastedText={this.handlePastedText}
          />
          <Button
            //color="#69a3ff"
            color="blue"
            size="small"
            loading={isLoading}
            disabled={isLoading}
            onClick={this.onSubmit}
          >
            <Icon name="edit" />
            Post thread
          </Button>

          <Button
            role="none"
            size="small"
            disabled={isLoading}
            onClick={this.onCancel}
          >
            <Icon name="cancel" />
            Clear
          </Button>
        </Form>
      </div>
    );
  }
}
