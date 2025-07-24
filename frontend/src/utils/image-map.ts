import LandingPageBAckgroundImage from "../assets/images/landing_page_background2.avif";
import LoginBackgroundImage from "../assets/images/login_background.jpeg";
import NotFoundImage from "../assets/images/not_found.webp";
import RegisterBackgroundImage from "../assets/images/register_background.jpeg";
import LogoImage from "../assets/logo/logo.jpg";
import EmptyHouseHoldImage from "../assets/images/empty_household.png";

export const ImageMap: { [key: string]: string } = {
  logo: LogoImage,
  login_background: LoginBackgroundImage,
  register_background: RegisterBackgroundImage,
  empty_house_hold: EmptyHouseHoldImage,
  landing_background_image: LandingPageBAckgroundImage,
  not_found: NotFoundImage,
};
export const getImage = (key: string): string => {
  return ImageMap[key] || LogoImage;
};
