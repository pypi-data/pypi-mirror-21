///% from  Linux Kernel v3.19.1/drivers/net/sungem_phy.c 
//////% First reset the PHY
sungem_phy_write(phy, MII_BMCR, ctl | BMCR_RESET);

//////% Select speed & duplex
switch(speed) {
case SPEED_10:
        break;
case SPEED_100:
        ctl |= BMCR_SPEED100;
        break;
case SPEED_1000:
default:
        return -EINVAL;
}

