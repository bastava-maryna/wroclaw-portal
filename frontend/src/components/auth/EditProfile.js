/* eslint-disable prettier/prettier */
import React, { useContext, useState, useEffect } from 'react';
import Dropzone from 'react-dropzone';
import { Form, Image, Message, Button, Grid } from 'semantic-ui-react';
import { imageUploadApi } from '../forum/ImageUploader';
import AuthContext from '../../context/auth/AuthContext';
import { editProfile } from '../../context/auth/AuthActions';
import StatusMessage from '../forum/StatusMessage';
import './style.css';

const EditProfile = ({ isLoading, error, editSuccess }) => {
  const { dispatch, user } = useContext(AuthContext);

  console.log('initial user data in edit profile');
  console.log(user);

  const [avatar, setAvatar] = useState(user.avatar);
  const [imgSrc, setImgSrc] = useState(null);
  const [values, setValues] = useState({
    //name: name,
    newPassword: '',
    currentPassword: '',
    avatarFile: null,
    avatarError: null,
    avatarUploading: false,
  });
  const handleChange = (e, { name, value }) => {
    setValues({ ...values, [name]: value });
  };

  const onImageDrop = (files) => {
    const currentFile = files[0];
    const reader = new FileReader();
    reader.addEventListener(
      'load',
      () => {
        console.log(reader.result);
        setImgSrc(reader.result);
      },
      false
    );
    reader.readAsDataURL(currentFile);
    setValues({ ...values, avatarFile: files[0] });
  };
  /*
  const onImageDrop = useCallback((acceptedFiles) => {
    acceptedFiles.forEach((file) => {
      const reader = new FileReader();

      reader.onabort = () => console.log('file reading was aborted');
      reader.onerror = () => console.log('file reading has failed');
      reader.onload = () => {
        // Do whatever you want with the file contents
        const binaryStr = reader.result;
        console.log(binaryStr);
      };
      reader.readAsArrayBuffer(file);
    });
    setValues({ ...values, avatarFile: acceptedFiles[0] });
  }, []);
  */
  const handleEditProfile = async () => {
    const password =
      values.newPassword !== '' ? values.newPassword : values.currentPassword;
    const newProfile = {
      user_name: user.user_name,
      user_email: user.user_email,
      password: password,
      avatar: avatar,
    };

    await dispatch(editProfile(dispatch, newProfile, user.user_id));

    setValues({ ...values, currentPassword: '' });
  };

  useEffect(() => {
    if (values.avatarUploading || values.avatarFile == null) return;
    console.log('in use effect');
    console.log(avatar);
    console.log('updated values');
    console.log(values);
    handleEditProfile();
  }, [avatar]);

  const handleSubmit = (e) => {
    e.preventDefault();
    const { currentPassword, avatarFile } = values;

    if (currentPassword !== '') {
      if (!avatarFile) {
        console.log('no new avatar');
        // no new avatar
        handleEditProfile();
      } else {
        setValues({ ...values, avatarUploading: true });

        imageUploadApi(avatarFile)
          .then((response) => {
            console.log('response from imageUpload');
            console.log(response.data);
            const new_avatar = response.data.secure_url;

            setValues({
              ...values,
              avatarUploading: false,
            });

            setAvatar(new_avatar);
          })
          .catch((error) => {
            console.log('error in submit');
            console.log(error);
            setValues({
              ...values,
              avatarError: 'Image Upload Error',
              avatarFile: null,
              avatarUploading: false,
            });
          });
      }
    }
  };

  const statusMessage = (
    <StatusMessage
      error={error || values.avatarError}
      errorMessage={error || values.avatarError}
      loading={isLoading || values.avatarUploading}
      loadingMessage={'Editing your profile'}
      success={editSuccess}
      successMessage={'Your profile edit was successful'}
      type="modal"
    />
  );

  const avatarURL = values.avatarFile
    ? values.avatarFile.preview
    : avatar
    ? avatar
    : ' https://i.imgur.com/7o5cwt8.png';

  return (
    <div>
      <Message
        attached
        header="Edit Your Profile"
        content="Fill out any part of the form below to edit your profile"
      />
      {statusMessage}
      <Form className="attached segment">
        <Grid celled columns={2}>
          <Grid.Column>
            <Form.Field>
              <label>Profile picture</label>
              {imgSrc !== null ? (
                <div>
                  <Image
                    src={imgSrc}
                    alt="imageSource"
                    className="editProfile-avatar"
                  />
                </div>
              ) : (
                <Dropzone onDrop={onImageDrop} multiple={false}>
                  {({ getRootProps, getInputProps }) => {
                    return (
                      <div {...getRootProps()}>
                        <Image src={avatarURL} className="editProfile-avatar" />

                        <input name='avatar'{...getInputProps()}/>
                      </div>
                    );
                  }}
                </Dropzone>
              )}
              <label>Tap to choose anoter avatar</label>
            </Form.Field>
          </Grid.Column>
          <Grid.Column>
            <Form.Input
              required
              label="Current Password"
              type="password"
              name="currentPassword"
              value={values.currentPassword}
              onChange={handleChange}
            />
            <Form.Input
              label="New Password"
              type="password"
              name="newPassword"
              value={values.newPassword}
              onChange={handleChange}
            />
          </Grid.Column>
        </Grid>
        <Button
          color="blue"
          loading={isLoading}
          disabled={isLoading}
          onClick={handleSubmit}
        >
          Submit
        </Button>
      </Form>
    </div>
  );
};
export default EditProfile;
