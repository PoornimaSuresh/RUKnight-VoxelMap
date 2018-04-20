import numpy as np
import os

# Given pose (x, y, z, yaw, pitch, roll)


class Voxel:

    def __init__(self):
        self.vox_dim = (16, 16, 8)
        self.depth_dim = (720, 1280)
        self.pose = (0, 0, 0, 0, 0, 0)
        self.depth_min = 0
        self.depth_max = 42
        self.voxel = np.zeros(self.vox_dim)

    def set_pose(self, x, y, z, roll, pitch, yaw):
        self.pose = (x, y, z, roll, pitch, yaw)

    def depth_to_vox(self, depth_map):
        x_dim = self.vox_dim[0]
        y_dim = self.vox_dim[1]
        z_dim = self.vox_dim[2]

        # Depth range from the depth image
        z_depth_max = np.max(np.max(depth_map))
        z_depth_min = np.min(np.min(depth_map))

        # Depths will be compressed into the voxel
        z_range = z_depth_max - z_depth_min
        z_chunk_size = z_range / z_dim

        # 1280 x 720 should be compressed into 16 x 16
        x_range = self.depth_dim[1]
        y_range = self.depth_dim[0]

        x_chunk_size = x_range / x_dim  # take chunks of 80
        y_chunk_size = y_range / y_dim

        depth_map_comp = np.zeros((x_dim, y_dim))
        temp_depth_map = np.zeros((x_range, y_dim))

        # Compress to a 16 x 16 depth map
        row_idx = 0
        j = 0
        for row in depth_map:

            # Compress x dimension from 1280 to 16 by averaging
            for i in range(x_dim):
                # print(i)
                # print((row[int(i * x_chunk_size):int((i + 1) * x_chunk_size)]))
                # print(len(row[int(i*x_chunk_size):int((i+1)*x_chunk_size)]))
                new_avg = np.average(row[int(i*x_chunk_size):int((i+1)*x_chunk_size)])
                temp_depth_map[j][i] = new_avg
                # print(temp_depth_map[j])

            # Compress y dimension from 720 to 16 by averaging
            if j % y_chunk_size == y_chunk_size - 1:
                # print(int(y_chunk_size) + 1)
                # print(np.average(temp_depth_map[j - int(y_chunk_size) + 1:j], axis=0))
                depth_map_comp[row_idx] = np.average(temp_depth_map[j - int(y_chunk_size) + 1:j], axis=0)
                row_idx += 1

            j += 1

        # print("Depth map compressed: ")
        # print(depth_map_comp)

        # Scale the z's from 0 to 8
        depth_map_comp = depth_map_comp * float(z_dim)/(self.depth_max - self.depth_min)
        # print("Depth map compressed & scaled: ")
        # print(depth_map_comp)

        voxel = np.zeros((x_dim, y_dim, z_dim))

        # Convert compressed depth map into 16 x 16 x 8 voxel
        for i in range(x_dim):
            for j in range(y_dim):
                z = int(np.round(depth_map_comp[i][j]))
                voxel[i][j][z] = 1

        self.voxel = voxel
        # print(voxel)

        
# Test with a randomly generated depth map:
'''
v = Voxel()

# depth_frame = np.zeros((720, 1280))
# depth_frame = [int.from_bytes(os.urandom(1), byteorder='little') for j in (for i in depth_frame)]
# depth_frame[True] = int.from_bytes(os.urandom(1), byteorder='little')
# for i in range(depth_frame.shape[0]):
#     r = int.from_bytes(os.urandom(1), byteorder='little')
#     for j in range(depth_frame.shape[1]):
#         depth_frame[i][j] = r

depth_frame = np.random.randint(0, 50, (720, 1280))

# print(depth_frame[0][0:80])
print(v.depth_to_vox(depth_frame))
'''


