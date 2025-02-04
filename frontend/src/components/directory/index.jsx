import React from "react";
import MenuItem from "../menu-item";

import skincareBg from '../../assets/skincare-bg.avif';
import fragranceBg from '../../assets/fragrance-bg.avif';
import miscellaneousBg from "../../assets/miscellaneous-bg.png";
import haircareBg from "../../assets/haircare-bg.webp";
import makeupBg from "../../assets/makeup-bg.avif";

import "./directory.styles.scss";

const Directory = () => {
    return (
        <section id="categories-section" className="directory-container">
            <div className="directory-menu">
                <MenuItem imageUrl={miscellaneousBg} productCategory={"Miscellaneous"} linkUrl={'/miscellaneous'} />
                <MenuItem imageUrl={makeupBg} productCategory={"Makeup"} linkUrl={'/makeup'} />
                <MenuItem imageUrl={skincareBg} productCategory={"Skincare"} linkUrl={'/skincare'} />
                <MenuItem imageUrl={haircareBg} productCategory={"Haircare"} linkUrl={'/haircare'} />
                <MenuItem imageUrl={fragranceBg} productCategory={"Fragrance"} linkUrl={'/fragrance'} />
            </div>
        </section>
    )
}

export default Directory;
