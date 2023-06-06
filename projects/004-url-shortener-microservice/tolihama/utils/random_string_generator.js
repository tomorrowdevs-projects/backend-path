class RandomStringGenerator {
    genRandomString = length => {
        const chars = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
        return Array.from({ length }, () => chars[this.rand(0, chars.length - 1)]).join('');
    }
    
    rand(min, max) {
        return Math.floor(Math.random() * (max - min + 1) + min);
    }
}

module.export = new RandomStringGenerator;