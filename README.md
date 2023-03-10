# image_file_viewer & image_file_cropping

## Image Viewer
![](readme_image_files/image_viewer.png)

### 1. listWidget
- Directory 리스트를 보여주는 텍스트 리스트 위젯
![](readme_image_files/directory_list_widget.png)

### 2. Directory file list Button
- 현재 viewer directory 내의 파일 조회
![](readme_image_files/view_file_list_button.png)

### 3. 현재 조회 사진 경로 및 파일명 위젯
![](readme_image_files/current_file_name_view.png)

### 4. 조회한 이미지를 보여주는 라벨
![](readme_image_files/view_image_label.png)

### 5. 리스트에서 이전 이미지를 조회하는 버튼
![](readme_image_files/left_button.png)
- 키보드 F3로 동작 가능

### 6. 리스트에서 이전 이미지를 조회하는 버튼
![](readme_image_files/right_button.png)
- 키보드 F4로 동작 가능

### 7. 단일 파일 등록
![](readme_image_files/file_upload.png)
- Open Image: 현재 PC내의 이미지를 불러오는 기능
![](readme_image_files/file_upload_2.png)
- PNG파일 또는 JPG파일만 허용하였음

### 8. 다중 파일(디렉토리) 등록
![](readme_image_files/file_upload.png)
- Open Directory: 현재 PC내의 이미지가 담긴 폴더를 불러오는 기능
![](readme_image_files/file_upload_3.png)
- 폴더 선택 가능

## Image Cropping
![](readme_image_files/image_cropping.png)

### 1. Row Line Edit
![](readme_image_files/Row_Column_Input_Button.png)
- Row 입력할 수 있는 박스형 라인

### 2. Column Line Edit
![](readme_image_files/Row_Column_Input_Button.png)
- Column 입력할 수 있는 박스형 라인

### 3. File Select Button
![](readme_image_files/file_selection_button.png)
- JPG, PNG파일을 선택할 수 있는 버튼

### 4. Input Row & Column Button
[](readme_image_files/Row_Column_Input_Button.png)
- 1, 2번에 입력한 숫자를 적용하는 버튼

### 5. Column - Row 디렉토리 생성 버튼
![](readme_image_files/generate_cropping_directory.png)
- 1, 2, 3, 4를 모두 적용한 후 사용할 수 있으며, 파일의 경로 및 Row, Column을 가져와 Column x Row의 수만큼 이미지를 분할해 디렉토리를 생성해주는 버튼
![](readme_image_files/generate_sample.png)
  - Column:3, Row:2, demo file을 cropping 한 화면

### 6. Row & Column 확인할 수 있는 Label
![](readme_image_files/confirm_row_column.png)
- Row와 Column의 입력값을 확인할 수 있는 라벨

### 7. 선택한 파일 이미지를 보여주는 라벨
![](readme_image_files/view_image_2.png)