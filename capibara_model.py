import pygame
import numpy as np

class Capibara:
    def __init__(self, scale=2):
        self.scale = scale
        self.colors = {
            'body': (139, 69, 19),
            'outline': (101, 67, 33),
            'belly': (241, 196, 144),
            'nose': (200, 150, 140),
            'black': (0, 0, 0),
            'white': (255, 255, 255)
        }

    def draw(self, screen, pos, time_factor, on_ground):
        scale = self.scale
        bob = np.sin(time_factor * 1.5) * 2.0 * scale

        upper_offset_x = np.sin(time_factor * 1.5) * 5 * scale
        lower_offset_x = -upper_offset_x

        rotation_angle = np.sin(time_factor * 1.0) * 0.2
        surf_width = 700
        surf_height = 700
        capibara_surf = pygame.Surface((surf_width, surf_height), pygame.SRCALPHA)
        center_x = surf_width // 2
        center_y = surf_height // 2

        x, y = center_x, center_y

        # Torso superior
        body_w = 100 * scale
        body_h = 250 * scale
        upper_body_h = 120 * scale
        upper_body_rect = pygame.Rect(int(x - body_w/2 + upper_offset_x), int(y - body_h/2 + bob + 30 * scale), int(body_w), int(upper_body_h))
        upper_outline_rect = upper_body_rect.inflate(12 * scale, 12 * scale)
        pygame.draw.ellipse(capibara_surf, self.colors['outline'], upper_outline_rect)
        pygame.draw.ellipse(capibara_surf, self.colors['body'], upper_body_rect)

        # Torso inferior
        lower_body_h = 130 * scale
        lower_body_w = body_w + 10 * scale
        lower_body_rect = pygame.Rect(int(x - lower_body_w/2 + lower_offset_x), int(y - body_h/2 + bob + upper_body_h - 60 * scale), int(lower_body_w), int(lower_body_h))
        lower_outline_rect = lower_body_rect.inflate(12 * scale, 12 * scale)
        pygame.draw.ellipse(capibara_surf, self.colors['outline'], lower_outline_rect)
        pygame.draw.ellipse(capibara_surf, self.colors['body'], lower_body_rect)

        # Barriga
        belly_rect = lower_body_rect.inflate(-40 * scale, -50 * scale)
        pygame.draw.ellipse(capibara_surf, self.colors['belly'], belly_rect)

        # Cabeza
        head_w = 70 * scale
        head_h = 60 * scale
        head_x = x + upper_offset_x
        head_y = y - body_h/2 + 40 * scale + bob
        head_rect = pygame.Rect(int(head_x - head_w/2), int(head_y - head_h/2), int(head_w), int(head_h))
        pygame.draw.ellipse(capibara_surf, self.colors['outline'], head_rect.inflate(10 * scale, 10 * scale))
        pygame.draw.ellipse(capibara_surf, self.colors['body'], head_rect)

        # Orejas
        ear_w, ear_h = 26 * scale, 36 * scale
        left_ear = pygame.Rect(int(head_x - 30 * scale - ear_w/2), int(head_y - 40 * scale), int(ear_w), int(ear_h))
        right_ear = pygame.Rect(int(head_x + 30 * scale - ear_w/2), int(head_y - 40 * scale), int(ear_w), int(ear_h))
        pygame.draw.ellipse(capibara_surf, self.colors['outline'], left_ear.inflate(6 * scale, 6 * scale))
        pygame.draw.ellipse(capibara_surf, self.colors['body'], left_ear)
        pygame.draw.ellipse(capibara_surf, self.colors['outline'], right_ear.inflate(6 * scale, 6 * scale))
        pygame.draw.ellipse(capibara_surf, self.colors['body'], right_ear)

        # Ojos
        eye_y = head_y - 5 * scale
        eye_x_offset = 18 * scale
        pygame.draw.circle(capibara_surf, self.colors['black'], (int(head_x - eye_x_offset), int(eye_y)), int(4 * scale))
        pygame.draw.circle(capibara_surf, self.colors['black'], (int(head_x + eye_x_offset), int(eye_y)), int(4 * scale))

        # Nariz
        nose_w, nose_h = 18 * scale, 12 * scale
        nose_rect = pygame.Rect(int(head_x - nose_w/2), int(head_y + 2 * scale), int(nose_w), int(nose_h))
        pygame.draw.ellipse(capibara_surf, self.colors['outline'], nose_rect.inflate(4 * scale, 4 * scale))
        pygame.draw.ellipse(capibara_surf, self.colors['nose'], nose_rect)

        # Boca
        mouth_y = head_y + 20 * scale
        pygame.draw.line(capibara_surf, self.colors['outline'], (head_x, mouth_y-10), (head_x, mouth_y + 5 * scale), int(3 * scale))
        pygame.draw.arc(capibara_surf, self.colors['outline'], (head_x - 10 * scale, mouth_y - 10, 10 * scale, 15 * scale), 3.14, 0, int(1 * scale))
        pygame.draw.arc(capibara_surf, self.colors['outline'], (head_x, mouth_y - 10, 10 * scale, 15 * scale), 3.14, 0, int(1 * scale))

        # Bigotes
        whisker_length = 20 * scale
        whisker_thickness = 1
        left_start_x = head_x - 10 * scale
        left_start_y_base = head_y + 12 * scale
        for i in range(3):
            y_offset = (i - 1) * 5 * scale
            start = (int(left_start_x), int(left_start_y_base + y_offset))
            end = (int(left_start_x - whisker_length), int(left_start_y_base + y_offset))
            pygame.draw.line(capibara_surf, self.colors['outline'], start, end, whisker_thickness)
        right_start_x = head_x + 10 * scale
        right_start_y_base = head_y + 12 * scale
        for i in range(3):
            y_offset = (i - 1) * 5 * scale
            start = (int(right_start_x), int(right_start_y_base + y_offset))
            end = (int(right_start_x + whisker_length), int(right_start_y_base + y_offset))
            pygame.draw.line(capibara_surf, self.colors['outline'], start, end, whisker_thickness)

        # Patas delanteras
        paw_w, paw_h = 36 * scale, 24 * scale
        front_y = head_y + 26 * scale
        front_x_offset = 45 * scale
        upper_len = 28 * scale
        lower_len = 26 * scale
        arm_thickness = int(12 * scale)

        def draw_arm(shoulder_x, shoulder_y, phase_offset):
            angle = np.sin(time_factor * 1.5 + phase_offset) * 0.5
            elbow_dx = int(np.sin(angle) * upper_len)
            elbow_dy = int(np.cos(angle) * upper_len)
            elbow = np.array([shoulder_x + elbow_dx, shoulder_y + elbow_dy])

            angle2 = angle + 0.4 * np.sin(time_factor * 1.5 + phase_offset)
            hand_dx = int(np.sin(angle2) * lower_len)
            hand_dy = int(np.cos(angle2) * lower_len)
            hand = np.array([elbow[0] + hand_dx, elbow[1] + hand_dy])

            pygame.draw.line(capibara_surf, self.colors['outline'], (shoulder_x, shoulder_y), tuple(elbow.astype(int)), arm_thickness)
            pygame.draw.line(capibara_surf, self.colors['outline'], tuple(elbow.astype(int)), tuple(hand.astype(int)), arm_thickness)
            pygame.draw.line(capibara_surf, self.colors['body'], (shoulder_x, shoulder_y), tuple(elbow.astype(int)), max(1, arm_thickness - 2))
            pygame.draw.line(capibara_surf, self.colors['body'], tuple(elbow.astype(int)), tuple(hand.astype(int)), max(1, arm_thickness - 2))

            pygame.draw.circle(capibara_surf, self.colors['body'], tuple(elbow.astype(int)), int(arm_thickness / 2))

            hand_rect = pygame.Rect(0, 0, int(paw_w), int(paw_h))
            hand_rect.center = (int(hand[0]), int(hand[1]))
            pygame.draw.ellipse(capibara_surf, self.colors['outline'], hand_rect.inflate(int(4 * scale), int(4 * scale)))
            pygame.draw.ellipse(capibara_surf, self.colors['body'], hand_rect)

        shoulder_y = int(head_y + 20 * scale)
        left_shoulder_x = int(x - front_x_offset + 6 * scale) + upper_offset_x
        right_shoulder_x = int(x + front_x_offset - 6 * scale) + upper_offset_x

        draw_arm(left_shoulder_x, shoulder_y, 0.0)
        draw_arm(right_shoulder_x, shoulder_y, 1.5)

        # Piernas traseras
        hip_x_offset = 20 * scale
        hip_y = int(y + 60 * scale + bob)
        upper_leg = 36 * scale
        lower_leg = 38 * scale
        leg_thickness = int(14 * scale)

        def draw_leg(hip_x, hip_y, phase, on_ground, time_factor):
            if on_ground:
                target_x = np.sin(time_factor * 1.5 + phase) * 30 * scale
                target_world_x = hip_x + target_x
                target_y = self.get_ground_y(target_world_x) - hip_y + 100
                L1 = upper_leg
                L2 = lower_leg
                d = np.sqrt(target_x**2 + target_y**2)
                if d <= L1 + L2 and d >= abs(L1 - L2):
                    cos_a2 = (target_x**2 + target_y**2 - L1**2 - L2**2) / (2 * L1 * L2)
                    a2 = np.arccos(np.clip(cos_a2, -1, 1))
                    a1 = np.arctan2(target_y, target_x) - np.arctan2(L2 * np.sin(a2), L1 + L2 * np.cos(a2))
                    angle1 = a1
                    angle2 = a1 + a2
                else:
                    angle1 = -0.2 + np.sin(time_factor * 1.5 + phase) * 0.3
                    angle2 = angle1 + 0.9 - 0.3 * np.cos(time_factor * 1.5 + phase)
            else:
                angle1 = -0.2 + np.sin(time_factor * 1.5 + phase) * 0.2
                angle2 = angle1 + 0.6 - 0.2 * np.cos(time_factor * 1.5 + phase)

            knee_dx = int(np.sin(angle1) * upper_leg)
            knee_dy = int(np.cos(angle1) * upper_leg)
            knee = np.array([hip_x + knee_dx, hip_y + knee_dy])

            foot_dx = int(np.sin(angle2) * lower_leg)
            foot_dy = int(np.cos(angle2) * lower_leg)
            foot = np.array([knee[0] + foot_dx, knee[1] + foot_dy])

            pygame.draw.line(capibara_surf, self.colors['outline'], (hip_x, hip_y), tuple(knee.astype(int)), leg_thickness)
            pygame.draw.line(capibara_surf, self.colors['outline'], tuple(knee.astype(int)), tuple(foot.astype(int)), leg_thickness)
            pygame.draw.line(capibara_surf, self.colors['body'], (hip_x, hip_y), tuple(knee.astype(int)), max(1, leg_thickness - 2))
            pygame.draw.line(capibara_surf, self.colors['body'], tuple(knee.astype(int)), tuple(foot.astype(int)), max(1, leg_thickness - 2))

            pygame.draw.circle(capibara_surf, self.colors['body'], (int(hip_x), int(hip_y)), int(leg_thickness / 2))
            pygame.draw.circle(capibara_surf, self.colors['body'], tuple(knee.astype(int)), int(leg_thickness / 2))

            foot_rect = pygame.Rect(0, 0, int(34 * scale), int(18 * scale))
            foot_rect.center = (int(foot[0]), int(foot[1]))
            pygame.draw.ellipse(capibara_surf, self.colors['outline'], foot_rect.inflate(int(4 * scale), int(4 * scale)))
            pygame.draw.ellipse(capibara_surf, self.colors['body'], foot_rect)

        left_hip_x = int(x - hip_x_offset) + lower_offset_x
        right_hip_x = int(x + hip_x_offset) + lower_offset_x
        draw_leg(left_hip_x, hip_y, 0.0, on_ground, time_factor)
        draw_leg(right_hip_x, hip_y, 1.6, on_ground, time_factor)

        # Ojos con brillo
        pygame.draw.circle(capibara_surf, self.colors['white'], (int(head_x - eye_x_offset + 3 * scale), int(eye_y - 2 * scale)), int(1 * scale))
        pygame.draw.circle(capibara_surf, self.colors['white'], (int(head_x + eye_x_offset + 3 * scale), int(eye_y - 2 * scale)), int(1 * scale))

        rotated_surf = pygame.transform.rotate(capibara_surf, np.degrees(rotation_angle))
        scale_x = 1 - abs(rotation_angle) * 0.4
        scaled_width = int(rotated_surf.get_width() * scale_x)
        scaled_surf = pygame.transform.scale(rotated_surf, (scaled_width, rotated_surf.get_height()))
        screen.blit(scaled_surf, (pos[0] - scaled_surf.get_width()//2, pos[1] - rotated_surf.get_height()//2))

    def get_ground_y(self, x):
        # Asumiendo WIDTH es accesible, pero para simplicidad, hardcode o pasar como param
        # Para este refactor, asumir WIDTH=900
        return 700 - 150 + (x / 900) * 50