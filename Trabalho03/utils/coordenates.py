import glm

def planet_to_world_coordenates(lat, lon, radius, center):
    lat_rad = glm.radians(lat) # Convertendo latitude para radianos
    lon_rad = glm.radians(lon) # Convertendo longitude para radianos

    x = center.x + radius * glm.cos(lat_rad) * glm.cos(lon_rad) # Calculando a coordenada x'
    y = center.y + radius * glm.cos(lat_rad) * glm.sin(lon_rad) # Calculando a coordenada y'
    z = center.z + radius * glm.sin(lat_rad) # Calculando a coordenada z'

    return glm.vec3(x, y, z) # Retornando as coordenadas 3D no espaço mundial


def get_rotation_angle_from_planet(pos, center):
    normal = glm.normalize(pos - center) # Calculando o vetor normal a partir da posição e do centro

    #precisamos da normal, um vetor tangente a esfera

    up = normal 
    reference = glm.vec3(0, 1, 0) # Vetor de referência para comparação (pode ser qualquer vetor não paralelo ao normal)
    
    right = glm.normalize(glm.cross(up, reference)) # Calculando o vetor right usando o produto vetorial
    forward = glm.normalize(glm.cross(right, up)) # Calculando o vetor forward usando o produto vetorial

    rotation = glm.mat4(1.0)

    rotation[0] = glm.vec4(right.x,   right.y,   right.z,   0.0)
    rotation[1] = glm.vec4(up.x,      up.y,      up.z,      0.0)
    rotation[2] = glm.vec4(forward.x, forward.y, forward.z, 0.0)
    rotation[3] = glm.vec4(0.0, 0.0, 0.0, 1.0)

    return rotation
