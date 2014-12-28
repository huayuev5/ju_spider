-- ----------------------------------------------------
SET SQL_MODE="NO_AUTO_VALUE_ON_ZERO";

-- ----------------------------------------------------
-- create database ju_db;
-- use ju_db;

-- ----------------------------------------------------
-- create table ju_brand_item

create table ju_brand_item(
    id bigint NOT NULL primary key auto_increment,
    name char(200) NOT NULL,
    description text,
    created datetime NOT NULL,
    updated datetime DEFAULT NULL,
    price double(16, 2),
    orig_price double(16, 2),
    started tinyint(1) NOT NULL DEFAULT '0',
    item_type char(10),
    brand_name char(100)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=100 ;

-- ----------------------------------------------------
-- create table ju_brand_item_num

create table ju_brand_item_num(
    id int NOT NULL primary key auto_increment,
    item_id bigint NOT NULL,
    sold_num int NOT NULL
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=100 ;

-- ----------------------------------------------------
-- create table ju_brand_item_detail

create table ju_brand_item_detail(
    id int NOT NULL primary key auto_increment,
    item_id bigint NOT NULL,
    img_src char(200),
    detail_src char(200)
) ENGINE=MyISAM  DEFAULT CHARSET=utf8 AUTO_INCREMENT=100 ;
