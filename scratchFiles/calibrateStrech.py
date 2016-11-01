import numpy as np

def extract_face_features(gray, detected_face, offset_coefficients):
    (x, y, w, h) = detected_face
    horizontal_offset = offset_coefficients[0] * w
    vertical_offset = offset_coefficients[1] * h
    extracted_face = gray[y+vertical_offset:y+h, 
                      x+horizontal_offset:x-horizontal_offset+w]
    new_extracted_face = zoom(extracted_face, (64. / extracted_face.shape[0], 
                                           64. / extracted_face.shape[1]))
    new_extracted_face = new_extracted_face.astype(float32)
    new_extracted_face /= float(new_extracted_face.max())
    return new_extracted_face

def make_map(facefile):
    c1_range = np.linspace(0, 0.35)
    c2_range = np.linspace(0, 0.3)
    result_matrix = np.nan * np.zeros_like(c1_range * c2_range[:, newaxis])
    gray, detected_faces = detect_face(cv2.imread(facefile))
    for face in detected_faces[:1]:
        for ind1, c1 in enumerate(c1_range):
            for ind2, c2 in enumerate(c2_range):
                extracted_face = extract_face_features(gray, face, (c1, c2))
                result_matrix[ind1, ind2] = predict_face_is_smiling(extracted_face)
    return (c1_range, c2_range, result_matrix)


r1 = make_map("noSmile.jpg")
r2 = make_map("smile.jpg")



figure(figsize=(12, 4))
subplot(131)
title('not smiling image')
pcolormesh(r1[0], r1[1], r1[2])
colorbar()
xlabel('horizontal stretch factor c1')
ylabel('vertical stretch factor c2')

subplot(132)
title('smiling image')
pcolormesh(r2[0], r2[1], r2[2])
colorbar()
xlabel('horizontal stretch factor c1')
ylabel('vertical stretch factor c2')

subplot(133)
title('correct settings for both images simultaneously')
pcolormesh(r1[0], r1[1], (r1[2]==0) & (r2[2]==1), cmap='gray')
colorbar()
xlabel('horizontal stretch factor c1')
ylabel('vertical stretch factor c2')

tight_layout()