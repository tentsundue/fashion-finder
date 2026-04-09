import { Box, FileUpload, Icon } from "@chakra-ui/react";
import { UploadOutlined } from "@ant-design/icons";


interface DropzoneProps {
  onFilesUploaded: (files: File[]) => void;
}

export default function Dropzone({ onFilesUploaded }: DropzoneProps) {
  
  return (
    <FileUpload.Root
      maxW="xl"
      alignItems="stretch"
      maxFiles={5}
      accept="image/png, image/jpeg, image/jpg"
      onFileChange={(upload) => {
        onFilesUploaded(upload.acceptedFiles);
      }}>
      <FileUpload.HiddenInput />
      <FileUpload.Dropzone>
        <Icon size="md" color="fg.muted">
          <UploadOutlined />
        </Icon>
        <FileUpload.DropzoneContent>
          <Box>Drag and drop files here</Box>
          <Box color="fg.muted">.png, .jpg, etc.</Box>
        </FileUpload.DropzoneContent>
      </FileUpload.Dropzone>
      <FileUpload.List clearable />
    </FileUpload.Root>
  );
}
