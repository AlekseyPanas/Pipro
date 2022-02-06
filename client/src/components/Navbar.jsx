const Navbar = () => {
  
  return (
    <nav className="bg-black shadow-lg sticky top-0 z-50">
      <div className="max-w-6xl m-auto align-middle px-4 py-4">
        <div className="flex justify-between">
          <div className="flex space-x-7">
            <div>
              <a href="#" className="flex items-center py-4 px-2">
                <span className="font-semibold text-gray-300 text-xl">
                  PIPRO
                </span>
              </a>
            </div>
          </div>
          <div className="hidden md:flex items-center space-x-3 ">
            <a
              href="https://github.com/AlekseyPanas/Pipro"
              target="_blank"
              className="py-2 px-2 font-medium text-gray-500 rounded hover:bg-green-500 hover:text-white transition duration-300"
            >
              View Repository
            </a>
            <a
              href=""
              target="_blank"
              className="flex items-center py-2 px-5 font-medium text-white bg-green-500 rounded hover:bg-green-400 transition duration-300"
            >
              Team
              <svg
                xmlns="http://www.w3.org/2000/svg"
                className="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M17 8l4 4m0 0l-4 4m4-4H3"
                />
              </svg>
            </a>
          </div>
          <div className="md:hidden flex items-center">
            <button className="outline-none mobile-menu-button">
              <svg
                className=" w-6 h-6 text-gray-500 hover:text-green-500 "
                x-show="!showMenu"
                fill="none"
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path d="M4 6h16M4 12h16M4 18h16"></path>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
}

export default Navbar;