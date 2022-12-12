import axios from 'axios';
const CLOUDINARY_UPLOAD_TRANSFORM_PRESET = 'wp-preset-transform-1'; // img transformed to 200x200
const CLOUDINARY_UPLOAD_PRESET = 'wp-preset-1';
const CLOUDINARY_UPLOAD_URL =
  'https://api.cloudinary.com/v1_1/wroclaw-portal/upload';

export const imageUploadApi = async (file, transform = true) => {
  const formData = new FormData();
  formData.append('file', file);
  const upload_preset = transform
    ? CLOUDINARY_UPLOAD_TRANSFORM_PRESET
    : CLOUDINARY_UPLOAD_PRESET;
  formData.append('upload_preset', upload_preset);
  return await axios.post(CLOUDINARY_UPLOAD_URL, formData, null);
};
